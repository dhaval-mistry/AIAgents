"""Real semantic embeddings through the Bedrock Runtime API, not chat completions."""
from dataclasses import dataclass
import json
import os
import numpy as np

# Present embedding failures through a domain-specific exception so callers do
# not need to understand boto3 or NumPy implementation details.
class EmbeddingError(RuntimeError):
    pass

# Describe the embedding space. Model ID, dimensions, and normalization must
# remain identical when building and querying an index.
@dataclass(frozen=True)
class EmbeddingConfig:
    model_id: str = 'amazon.titan-embed-text-v2:0'
    dimensions: int = 1024
    region: str = 'us-west-2'

    @classmethod
    # Read and validate supported Titan settings from the environment.
    def from_env(cls):
        try:
            dimensions = int(os.getenv('BEDROCK_EMBEDDING_DIMENSIONS', '1024'))
        except ValueError:
            raise EmbeddingError('BEDROCK_EMBEDDING_DIMENSIONS must be 256, 512, or 1024.') from None
        model = os.getenv('BEDROCK_EMBEDDING_MODEL_ID', 'amazon.titan-embed-text-v2:0')
        if model != 'amazon.titan-embed-text-v2:0' or dimensions not in (256, 512, 1024):
            raise EmbeddingError('This adapter supports Titan Text Embeddings V2 with 256, 512, or 1024 dimensions.')
        region = os.getenv('BEDROCK_EMBEDDING_REGION') or os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION') or 'us-west-2'
        return cls(model, dimensions, region)

    # Return only properties that affect vector compatibility and cache keys.
    def identity(self):
        # Region is an access setting; the embedding space depends on model/config.
        return {'model_id': self.model_id, 'dimensions': self.dimensions, 'normalize': True}


# Convert provider or cached output into a finite, unit-length float32 vector.
def normalized_vector(value, dimensions):
    vector = np.asarray(value, dtype=np.float32)
    if vector.shape != (dimensions,) or not np.isfinite(vector).all():
        raise EmbeddingError('Embedding has invalid dimensions or non-finite numbers.')
    norm = float(np.linalg.norm(vector))
    if norm <= 0:
        raise EmbeddingError('Embedding contains no usable values.')
    return vector / norm


# Lazily call Titan Text Embeddings V2 through Bedrock Runtime.
class BedrockEmbedder:
    # Allow tests or callers to inject configuration and a fake/runtime client.
    def __init__(self, config=None, client=None):
        self.config = config or EmbeddingConfig.from_env()
        self._client = client

    @property
    # Delay boto3 client creation until an embedding is actually requested.
    def client(self):
        if self._client is None:
            import boto3
            from botocore.config import Config
            # Standard AWS credential chain, including profiles, IAM roles, or
            # environment credentials. Botocore also supports Bedrock bearer tokens
            # through AWS_BEARER_TOKEN_BEDROCK with a compatible installed SDK.
            self._client = boto3.client(
                'bedrock-runtime', region_name=self.config.region,
                config=Config(connect_timeout=10, read_timeout=45,
                              retries={'mode': 'standard', 'total_max_attempts': 4}),
            )
        return self._client

    # Validate input, request one normalized embedding, and sanitize failures so
    # prompts, response bodies, and credentials never appear in logs.
    def embed(self, text):
        if not isinstance(text, str) or not text.strip():
            raise EmbeddingError('Cannot embed empty text.')
        # Conservative bound below Titan's character and token limits, even for
        # languages that tokenize less efficiently than English.
        if len(text) > 6000:
            raise EmbeddingError('Embedding input exceeds 6000 characters; split the document further.')
        try:
            response = self.client.invoke_model(
                modelId=self.config.model_id,
                contentType='application/json', accept='application/json',
                body=json.dumps({'inputText': text, 'dimensions': self.config.dimensions,
                                 'normalize': True, 'embeddingTypes': ['float']}),
            )
            body = response['body']
            try:
                payload = json.loads(body.read())
            finally:
                body.close()
            return normalized_vector(payload['embedding'], self.config.dimensions)
        except EmbeddingError:
            raise
        except Exception as error:
            # Report only the provider's error CODE, never requests, prompts,
            # response bodies, access keys, or exception messages.
            response = getattr(error, 'response', {})
            code = response.get('Error', {}).get('Code', type(error).__name__)
            raise EmbeddingError(
                f'Bedrock embedding request failed ({code}). Check region, credentials, '
                'Titan model availability, and bedrock:InvokeModel permission.'
            ) from None
