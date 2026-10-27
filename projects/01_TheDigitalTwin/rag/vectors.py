"""Semantic-only cosine search over a local, self-contained NumPy snapshot."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
from datetime import datetime, timezone
import numpy as np
from rag.settings import (CHUNK_WORDS, CHUNK_OVERLAP, INDEX_DIR, CACHE_DIR,
                          MAX_MATCHES, MIN_SIMILARITY)
from rag.embeddings import BedrockEmbedder, normalized_vector

FORMAT = 'bedrock-titan-semantic-v1'

# Distinguish an unusable semantic snapshot from provider embedding failures.
class IndexError(RuntimeError):
    """Missing, corrupt, or incompatible semantic index."""


# Write a complete byte payload to a temporary file, flush it, and atomically
# replace the destination so readers never observe a partial index generation.
def atomic_bytes(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.write-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


# Serialize human-readable metadata using the same atomic-write guarantee.
def atomic_json(path, data):
    atomic_bytes(path, json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))


# Split normalized source documents into overlapping, bounded passages while
# retaining source metadata needed for citations and evaluation.
def make_chunks(documents, width=CHUNK_WORDS, overlap=CHUNK_OVERLAP):
    if width <= overlap or overlap < 0:
        raise ValueError('Chunk width must exceed non-negative overlap.')
    chunks = []
    for doc in documents:
        words = doc.get('text', '').split()
        if not words:
            continue
        # A short source overview in manual content can remain a complete passage.
        for start in range(0, len(words), width - overlap):
            text = ' '.join(words[start:start + width])
            # Bound by characters as well as words. Very long tokens must not
            # exceed the embedding adapter's input cap.
            for offset in range(0, len(text), 5000):
                part = text[offset:offset + 5000]
                chunk = {'title': str(doc.get('title', 'Untitled'))[:180],
                         'source': str(doc.get('source', 'local')),
                         'url': str(doc.get('url') or ''), 'text': part}
                chunk['id'] = hashlib.sha256(json.dumps(chunk, sort_keys=True).encode()).hexdigest()[:20]
                chunks.append(chunk)
            if start + width >= len(words):
                break
    return chunks


# Include the source title in embedding input to improve topical retrieval.
def embedding_text(chunk):
    return f"Title: {chunk['title']}\n{chunk['text']}"


# Tie a cached vector to both exact text and the embedding-space identity.
def cache_key(text, identity):
    return hashlib.sha256(json.dumps([identity, text], sort_keys=True).encode()).hexdigest()


# Embed every passage, reuse compatible checkpoints, and publish one validated,
# self-contained semantic snapshot only after the complete build succeeds.
def build_index(documents, directory=INDEX_DIR, embedder=None, cache_dir=CACHE_DIR, force=False):
    embedder = embedder or BedrockEmbedder()
    chunks = make_chunks(documents)
    if not chunks:
        raise IndexError('No source text found. Add Profile.pdf, summary.txt, or manual documents.')
    identity = embedder.config.identity()
    vectors, reused, generated = [], 0, 0
    for number, chunk in enumerate(chunks, 1):
        text = embedding_text(chunk)
        key = cache_key(text, identity)
        cache_file = Path(cache_dir) / f'{key}.json'
        vector = None
        if not force and cache_file.exists():
            try:
                entry = json.loads(cache_file.read_text(encoding='utf-8'))
                if entry['key'] == key and entry['identity'] == identity:
                    vector = normalized_vector(entry['vector'], embedder.config.dimensions)
            except (OSError, ValueError, KeyError, TypeError, RuntimeError):
                pass
        if vector is None:
            vector = normalized_vector(embedder.embed(text), embedder.config.dimensions)
            # Checkpoint every success so an interrupted refresh can resume.
            atomic_json(cache_file, {'key': key, 'identity': identity, 'vector': vector.tolist()})
            generated += 1
        else:
            reused += 1
        vectors.append(vector)
        if number % 25 == 0 or number == len(chunks):
            print(f'[embeddings] {number}/{len(chunks)} passages; {generated} generated, {reused} cached')
    metadata = {'format': FORMAT, **identity, 'passages': len(chunks),
                'created_at': datetime.now(timezone.utc).isoformat()}
    # The authoritative file contains vectors AND matching text/metadata, so
    # readers never combine one generation of text with another's vectors.
    import io
    stream = io.BytesIO()
    np.savez_compressed(stream, embeddings=np.stack(vectors).astype(np.float32),
                        chunks_json=np.array(json.dumps(chunks, ensure_ascii=False)),
                        metadata_json=np.array(json.dumps(metadata)))
    directory = Path(directory)
    atomic_bytes(directory / 'vectors.npz', stream.getvalue())
    # Human-readable mirrors, not runtime dependencies.
    atomic_json(directory / 'chunks.json', chunks)
    atomic_json(directory / 'metadata.json', metadata)
    return {'documents': len(documents), 'passages': len(chunks),
            'generated': generated, 'cached': reused}


# Load a compatible local snapshot and perform exact cosine-similarity search.
class LocalVectors:
    # Validate model metadata, matrix shape, normalization, and passage records
    # at startup so corrupt or stale indexes fail clearly instead of silently.
    def __init__(self, directory=INDEX_DIR, embedder=None):
        self.embedder = embedder or BedrockEmbedder()
        try:
            with np.load(Path(directory) / 'vectors.npz', allow_pickle=False) as snapshot:
                self.metadata = json.loads(str(snapshot['metadata_json'].item()))
                self.chunks = json.loads(str(snapshot['chunks_json'].item()))
                self.vectors = snapshot['embeddings'].astype(np.float32)
            if self.metadata.get('format') != FORMAT:
                raise ValueError('Not a semantic snapshot')
            for key, value in self.embedder.config.identity().items():
                if self.metadata.get(key) != value:
                    raise ValueError('Embedding model/configuration mismatch')
            expected = (len(self.chunks), self.embedder.config.dimensions)
            if not self.chunks or self.vectors.shape != expected or not np.isfinite(self.vectors).all():
                raise ValueError('Invalid vector matrix')
            if self.metadata.get('passages') != len(self.chunks):
                raise ValueError('Passage metadata mismatch')
            lengths = np.linalg.norm(self.vectors, axis=1)
            if not np.allclose(lengths, 1, atol=1e-4):
                raise ValueError('Vectors are not normalized')
            for chunk in self.chunks:
                if not isinstance(chunk, dict) or not all(isinstance(chunk.get(k), str) for k in ('id','title','text','url','source')):
                    raise ValueError('Invalid passage metadata')
        except Exception as error:
            raise IndexError(
                f'No compatible semantic index ({type(error).__name__}). '
                'Run python refresh_knowledge.py locally, then deploy the rebuilt vectors.npz.'
            ) from None

    # Embed the query and return the highest-scoring passages above the optional
    # threshold; normalized vectors make the dot product equal cosine similarity.
    def search(self, question, limit=MAX_MATCHES, min_score=MIN_SIMILARITY):
        if limit <= 0:
            return []
        query = normalized_vector(self.embedder.embed(question), self.embedder.config.dimensions)
        scores = self.vectors @ query
        # There are no keyword routes, topic mappings, or phrase-based boosts.
        order = np.argsort(-scores, kind='stable')[:limit]
        return [{**self.chunks[int(idx)], 'score': round(float(scores[idx]), 5)}
                for idx in order if float(scores[idx]) >= min_score]
