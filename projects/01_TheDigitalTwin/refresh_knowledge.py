"""Collect content and create a real Bedrock semantic index on your laptop."""
import argparse
import json
from rag.settings import CONFIG_FILE, KNOWLEDGE_DIR, INDEX_DIR
from rag.sources import (local_documents, transcript_documents, fetch_medium,
                         fetch_github, fetch_youtube)
from rag.vectors import build_index, make_chunks, atomic_json
from rag.embeddings import BedrockEmbedder


# Merge local documents, optional public feeds, and last-known external cache
# into one deduplicated collection for previewing or indexing.
def collect(config, offline=False):
    docs = local_documents() + transcript_documents()
    print(f'[local] Read {len(docs)} documents')
    cache_file = KNOWLEDGE_DIR / 'external_cache.json'
    try:
        cache = json.loads(cache_file.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        cache = {}
    refreshed = {}
    sources = [
        ('medium', bool(config.get('medium_feed_url')), lambda: fetch_medium(config['medium_feed_url'], config.get('max_medium_articles', 20))),
        ('github', bool(config.get('github_username')), lambda: fetch_github(config['github_username'], config.get('max_github_repos', 12))),
        ('youtube', bool(config.get('youtube_channel_id')), lambda: fetch_youtube(config['youtube_channel_id'], config.get('max_youtube_videos', 20))),
    ]
    channel = config.get('youtube_channel_id', '')
    if channel and (not channel.startswith('UC') or len(channel) != 24):
        raise ValueError('youtube_channel_id must be the actual 24-character UC... channel ID, not an @handle or URL.')
    for name, enabled, fetch in sources:
        if not enabled:
            # Explicitly disabling a source removes old cached content from it.
            refreshed[name] = []
            print(f'[{name}] Disabled in sources.json')
        elif offline:
            refreshed[name] = cache.get(name, [])
            print(f'[{name}] Offline: using {len(refreshed[name])} cached documents')
        else:
            try:
                rows = fetch()
                refreshed[name] = rows if rows else cache.get(name, [])
                print(f'[{name}] {len(rows)} fetched; {len(refreshed[name])} available')
            except Exception as error:
                refreshed[name] = cache.get(name, [])
                print(f'[{name}] Fetch failed ({type(error).__name__}); using {len(refreshed[name])} cached documents')
        docs.extend(refreshed[name])
    atomic_json(cache_file, refreshed)
    # Same content from two sources can still retain distinct provenance.
    unique = {}
    for item in docs:
        if item.get('text', '').strip():
            unique[(item.get('source'), item.get('title'), item.get('url'), item['text'])] = item
    return list(unique.values())


# Parse refresh modes, validate provider access when requested, and coordinate
# preview or full semantic-index generation.
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Make one small, billable Titan request to verify access; no source collection')
    parser.add_argument('--preview', action='store_true', help='Collect sources and write source_preview.json; no embedding calls')
    parser.add_argument('--offline-sources', action='store_true', help='Skip public feed requests; use local content and cached feeds. Embeddings still require AWS.')
    parser.add_argument('--force', action='store_true', help='Regenerate embeddings, ignoring cached vectors; incurs usage for every passage')
    args = parser.parse_args()
    embedder = BedrockEmbedder()
    if args.check:
        vector = embedder.embed('Professional experience and technical expertise.')
        print(f'[OK] Titan connection works: {len(vector)} dimensions, region={embedder.config.region}')
        return
    config = json.loads(CONFIG_FILE.read_text(encoding='utf-8'))
    docs = collect(config, offline=args.offline_sources)
    if args.preview:
        atomic_json(KNOWLEDGE_DIR / 'source_preview.json', docs)
        print(f'[preview] {len(docs)} documents, {len(make_chunks(docs))} passages. No embedding API calls made.')
        print('Review knowledge/source_preview.json before sending content to Bedrock.')
        return
    result = build_index(docs, INDEX_DIR, embedder=embedder, force=args.force)
    print(f"[OK] {result['documents']} documents -> {result['passages']} semantic vectors")
    print(f"[OK] {result['generated']} new embedding requests; {result['cached']} cache hits")
    print(f'Index: {INDEX_DIR / "vectors.npz"}')
    print('Review chunks.json before committing. Restart app.py after refreshing.')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        from rag.embeddings import EmbeddingError
        if isinstance(error, (EmbeddingError, ValueError, FileNotFoundError)):
            print(f'[ERROR] {error}')
        else:
            print(f'[ERROR] Refresh failed ({type(error).__name__}). Previous runtime snapshot was not replaced unless embedding finished.')
        raise SystemExit(1)
