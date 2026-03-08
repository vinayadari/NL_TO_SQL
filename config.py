import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL
PG_HOST     = os.getenv("PG_HOST", "localhost")
PG_PORT     = os.getenv("PG_PORT", "5432")
PG_DATABASE = os.getenv("PG_DATABASE", "NLP_VOICE")
PG_USER     = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "")

# Ollama
OLLAMA_URL   = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:8b")

# MCP
MCP_PORT     = int(os.getenv("MCP_PORT", "8765"))
MCP_MAX_ROWS = int(os.getenv("MCP_MAX_ROWS", "500"))