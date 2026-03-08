# nl2sql-mcp

> Talk to your PostgreSQL database in plain English — fully offline, voice-friendly output.

---

## What It Does

Type (or speak) a question like:

```
"Show me the top 5 customers by total orders"
```

And get back:

```
Top 5 customers by total orders:
1. Alice   →  42 orders
2. Bob     →  38 orders
3. Carol   →  31 orders
4. David   →  27 orders
5. Eve     →  19 orders
```

No SQL knowledge needed. No internet required after setup.

---

## Features

| Feature | Details |
|---|---|
| 🧠 Natural Language → SQL | Powered by a local Ollama LLM |
| 🐘 PostgreSQL Queries | Runs real queries on your database |
| 🔌 MCP Protocol | Reliable, structured tool execution |
| 📡 100% Offline | Everything runs on your machine |
| 🔊 Voice-Friendly Output | Clean, readable — speakable via `--speak` |

---

## Project Structure

```
nl2sql-mcp/
├── main.py            # CLI entry point
├── config.py          # Settings and environment variables
├── schema_loader.py   # Reads your DB schema for the LLM
├── nl_to_sql.py       # Converts English to SQL via Ollama
├── mcp_server.py      # MCP protocol layer
├── db_executor.py     # Runs SQL safely on PostgreSQL
├── voice_output.py    # Formats output for display and speech
└── requirements.txt
```

---

## How It Works

```
Your Question
     ↓
nl_to_sql.py       →   Ollama LLM converts English to SQL
     ↓
mcp_server.py      →   MCP validates and routes the query
     ↓
db_executor.py     →   Executes SQL on PostgreSQL (read-only)
     ↓
voice_output.py    →   Returns clean, readable result
```

---

## Requirements

- Python 3.10+
- PostgreSQL (running locally or remote)
- [Ollama](https://ollama.com) installed and running

```bash
# Recommended model for best SQL accuracy
ollama pull sqlcoder
```

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/vinayadari/NL_TO_SQL.git
cd NL_TO_SQL

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up your environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials and Ollama model
```

---

## Configuration

Create a `.env` file in the root directory:

```env
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=mydb
PG_USER=postgres
PG_PASSWORD=yourpassword

OLLAMA_MODEL=sqlcoder
OLLAMA_URL=http://localhost:11434

MCP_PORT=8765
```

---

## Usage

**Interactive mode** (ask multiple questions):
```bash
python main.py
```

**Single question:**
```bash
python main.py "How many users signed up last month?"
```

**With voice output:**
```bash
python main.py --speak "Show all products under $50"
```

---

## Safety

- All queries run in **read-only transactions** — no accidental writes
- SQL is validated before execution — `DROP`, `DELETE`, `UPDATE`, `INSERT` are blocked
- Results are capped at **500 rows** by default

---

## Tech Stack

- [`psycopg2`](https://pypi.org/project/psycopg2-binary/) — PostgreSQL driver
- [`ollama`](https://pypi.org/project/ollama/) — Local LLM client
- [`mcp`](https://pypi.org/project/mcp/) — MCP protocol SDK
- [`tabulate`](https://pypi.org/project/tabulate/) — Table formatting
- [`pyttsx3`](https://pypi.org/project/pyttsx3/) — Offline text-to-speech
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) — Environment config

---

## Roadmap

- [ ] Support for MySQL and SQLite
- [ ] Web UI frontend
- [ ] Query history and favorites
- [ ] Multi-database switching
- [ ] Export results to CSV

---

## License

MIT — free to use, modify, and distribute.