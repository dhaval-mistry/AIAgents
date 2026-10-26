"""Shared configuration. No secrets belong in knowledge/sources.json."""
from pathlib import Path
import os
from dotenv import load_dotenv

# Resolve every data path from the source tree so commands work consistently
# regardless of the caller's current working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
# Use the project's environment without overriding Render's environment variables.
load_dotenv(PROJECT_ROOT / '.env', override=False)
KNOWLEDGE_DIR = PROJECT_ROOT / 'knowledge'
INDEX_DIR = KNOWLEDGE_DIR / 'index'
MANUAL_DIR = KNOWLEDGE_DIR / 'manual'
CONFIG_FILE = KNOWLEDGE_DIR / 'sources.json'
CACHE_DIR = PROJECT_ROOT / '.cache' / 'embeddings'

# Central retrieval limits keep prompts, history, and tool loops predictable.
CHUNK_WORDS = 170
CHUNK_OVERLAP = 35
MAX_MATCHES = 6
MAX_CONTEXT_CHARS = 10000
MAX_HISTORY_MESSAGES = 6
MAX_HISTORY_CHARS = 4000
MAX_QUESTION_CHARS = 2000
MAX_TOOL_ROUNDS = 3
# Zero means return nearest passages without pretending similarity proves relevance.
# Tune a positive threshold with your own labeled retrieval questions.
MIN_SIMILARITY = float(os.getenv('RAG_MIN_SIMILARITY', '0.0'))
# Known-safe defaults are used only when owner configuration does not override
# them with another valid HTTPS profile URL.
LINKS = {
    'linkedin': 'https://www.linkedin.com/in/dhavalmmistry/',
    'github': 'https://github.com/dhaval-mistry',
    'medium': 'https://medium.com/@mahantai',
    'youtube': 'https://www.youtube.com/@mahantaijournal',
}
