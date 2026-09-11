# AI-Powered Business Analytics Assistant

### Ask questions in plain English. Get validated data insights.

An AI-powered analytics system that lets **non-technical business users query operational data using natural language** instead of writing SQL.

A user can ask:

> **“Which warehouses had the highest order delays this month?”**

The system translates the question into SQL, validates the generated query, executes it safely against a database, analyzes the results, and returns a **result table, relevant visualization, and concise business takeaway**.

The project is intentionally presented as a **general business analytics system**, with an **Operations Analytics** dataset as the primary demonstration domain.

---

## 🎯 The Problem

Business users often know exactly **what they want to know**, but not **how to query the database to find it**.

An operations manager may ask:

- Which warehouses have the highest delay rate?
- Which region generated the most revenue?
- Which products are approaching stockout?
- Which suppliers have the worst delivery performance?
- Which locations are consistently missing their targets?
- How has order volume changed over the last few months?

These are business questions, not SQL questions.

The traditional workflow often looks like:

```text
Business question
      ↓
Ask analyst / data team
      ↓
Write SQL
      ↓
Export results
      ↓
Create chart
      ↓
Send report
      ↓
Make decision
```

For small and mid-sized teams without dedicated analysts, this creates friction and delays.

### The goal

Make the workflow:

```text
Business question
      ↓
Natural language
      ↓
AI-generated SQL
      ↓
SQL validation
      ↓
Safe database execution
      ↓
Result analysis
      ↓
Chart + insight
      ↓
Decision
```

The system does not try to replace business judgment.

It removes the repetitive technical work between a **business question** and the **data needed to answer it**.

---

# 💡 What the system does

The user interacts with the application conversationally.

### Example

**User:**

> Which warehouses had the highest order delays this month?

### System:

**Generated SQL**

```sql
SELECT
    warehouse,
    AVG(delay_rate) AS avg_delay
FROM orders
WHERE order_date >= ...
GROUP BY warehouse
ORDER BY avg_delay DESC;
```

**Result**

| Warehouse | Average Delay |
|---|---:|
| Warehouse B | 18.4% |
| Warehouse D | 14.7% |
| Warehouse A | 9.8% |

**Insight**

> Warehouse B has the highest average delay rate this month at 18.4%, significantly above the other warehouses.

**Visualization**

The system automatically selects an appropriate chart type based on the returned data.

The important part is that the user receives **the answer and the evidence behind the answer**.

---

# 🧠 Core Architecture

```text
                         USER
                           │
                           │
                           ▼
              ┌─────────────────────────┐
              │       React UI          │
              │ Natural-language input  │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │       LLM #1            │
              │    Natural Language     │
              │          → SQL          │
              │                         │
              │ Grounded on live schema │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │      SQL Safety Layer   │
              │                         │
              │ • sqlglot parsing       │
              │ • SELECT-only           │
              │ • table allowlist       │
              │ • row limits            │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │     Read-only DB        │
              │                         │
              │ SQLite / PostgreSQL     │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │        LLM #2           │
              │    Result Analysis      │
              │                         │
              │ • Business takeaway     │
              │ • Chart recommendation  │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │     Analytics UI        │
              │                         │
              │ KPI • Chart • Table     │
              │ SQL • Insight           │
              └─────────────────────────┘
```

The two LLM calls are deliberately separated:

```text
generate_sql()
      +
analyze_results()
```

This keeps SQL generation and result interpretation independently testable and allows changes to one prompt without silently changing the behavior of the other.

---

# 🔐 The Interesting Engineering Problem

Generating SQL with an LLM is relatively easy.

**Safely and reliably executing LLM-generated SQL is the harder problem.**

The system therefore treats generated SQL as **untrusted input**.

```text
User question
      ↓
LLM generates SQL
      ↓
Raw SQL
      ↓
sqlglot parser
      ↓
Safety checks
      │
      ├── Is it SELECT-only?
      ├── Are referenced tables allowed?
      ├── Are dangerous statements present?
      └── Is the result size capped?
      ↓
Safe SQL
      ↓
Read-only database
```

## Current SQL guardrails

Every generated query passes through validation before execution.

### 1. SELECT-only enforcement

The system rejects statements that can modify database state, including:

```text
INSERT
UPDATE
DELETE
DROP
ALTER
CREATE
TRUNCATE
```

### 2. Table allowlisting

The application checks the tables referenced by the generated query against an explicit allowlist.

### 3. Result limits

Queries are capped so unexpectedly large result sets do not get passed into the analysis model or frontend.

### 4. Static SQL parsing

`sqlglot` is used to parse the query into an AST before execution.

This makes it possible to inspect the structure of the generated query rather than treating it as an opaque string.

### 5. Read-only execution path

The application has no normal write path for generated analytics queries.

The intended production setup additionally uses a database role with only the required `SELECT` permissions.

---

# 📊 Evaluation — Measuring Actual Correctness

A natural-language SQL demo can look impressive while still producing incorrect answers.

This project therefore includes an **evaluation harness**.

Instead of asking:

> “Did the LLM generate SQL that looks correct?”

the evaluation asks:

> **“Did the generated SQL produce the same correct result as a hand-verified query?”**

Each benchmark case contains:

```text
question
    +
golden_sql
```

The evaluation pipeline is:

```text
                 Benchmark question
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
       Generated SQL            Golden SQL
             │                       │
             ▼                       ▼
       Validation                Database
             │                       │
             ▼                       ▼
          Results                Results
             │                       │
             └───────────┬───────────┘
                         ▼
               Semantic comparison
                         │
                         ▼
                      Accuracy
```

The harness compares **result sets rather than SQL text**.

This matters because two syntactically different SQL queries can still be logically equivalent and return the same correct result.

### Run the evaluation

```bash
cd backend
python eval_harness.py
```

The benchmark should grow to cover:

- Simple lookups
- Aggregations
- Grouping
- Date filtering
- Multi-table joins
- Operational performance questions
- Different natural-language formulations of the same question

The final accuracy number should be measured from the actual benchmark rather than claimed in advance.

---

# 🏗️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React + Vite | Analytics interface |
| Styling | Tailwind CSS | UI styling |
| Charts | Recharts | Data visualization |
| Backend | FastAPI | API and application layer |
| AI | Claude API | Natural-language understanding and analysis |
| ORM / DB layer | SQLAlchemy | Database abstraction |
| SQL parser | sqlglot | SQL validation and AST inspection |
| Local database | SQLite | Zero-setup development |
| Production database | PostgreSQL / Neon | Production deployment |
| Evaluation | Python benchmark harness | NL→SQL correctness measurement |

---

# 📂 Repository Structure

```text
ai-business-analytics/
│
├── backend/
│   ├── main.py
│   │   └── FastAPI application
│   │
│   ├── db.py
│   │   └── Database connection,
│   │       schema introspection,
│   │       and query execution
│   │
│   ├── llm.py
│   │   └── NL→SQL generation,
│   │       SQL validation,
│   │       and result analysis
│   │
│   ├── eval_harness.py
│   │   └── Accuracy benchmark
│   │
│   ├── seed_data.py
│   │   └── Synthetic operations dataset
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   └── React analytics dashboard
│
└── README.md
```

---

# 🚀 Setup

## Backend

```bash
cd backend

python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

Add the required API key:

```env
ANTHROPIC_API_KEY=your_api_key
```

Seed the local database:

```bash
python seed_data.py
```

Start the API:

```bash
uvicorn main:app --reload
```

Backend:

```text
http://localhost:8000
```

---

# 🧪 Test the API

Example:

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "average order delay by warehouse"}'
```

The API runs the complete pipeline:

```text
Question
   ↓
NL → SQL
   ↓
Validation
   ↓
Database
   ↓
Result analysis
   ↓
Response
```

---

# 🗄️ Database

The project is designed to use:

### Local development

```text
SQLite
```

### Production

```text
PostgreSQL / Neon
```

The SQLAlchemy abstraction keeps the application code largely independent of the underlying database.

To switch to a production database, configure:

```env
DATABASE_URL=...
```

No fundamental changes to the analytics pipeline should be required.

---

# 🔒 Production Security Extensions

The current validation layer provides a foundation, but a production analytics platform would require stronger authorization controls.

## Column-level authorization

Some fields may be sensitive.

For example:

```text
Manager
   ↓
Allowed columns
   ↓
Validated SQL
```

The application can inspect:

```text
parsed.find_all(exp.Column)
```

and verify requested columns against a role-specific allowlist.

---

## Row-level authorization

A regional manager may only be allowed to view their region.

Instead of trusting the LLM to generate:

```sql
WHERE region = 'South'
```

the application should enforce the restriction itself.

Conceptually:

```text
User identity
     ↓
Authorized region
     ↓
SQL AST modification
     ↓
Validated query
     ↓
Database
```

This prevents the model from becoming the authorization layer.

---

## Additional production controls

Potential extensions include:

- Database roles with `SELECT` grants only
- Statement timeouts
- Query audit logging
- User/role-based access control
- Column-level authorization
- Row-level restrictions
- Query monitoring
- Rate limiting
- Prompt and response logging
- Sensitive-data filtering

---

# 🧩 Why Two LLM Calls?

A single prompt could theoretically generate both SQL and the final explanation.

The project intentionally separates these responsibilities.

```text
LLM #1
Natural language
      ↓
SQL

LLM #2
Query results
      ↓
Business insight + chart recommendation
```

### Benefits

**Focused prompts**

Each model call has one responsibility.

**Independent testing**

SQL generation can be evaluated separately from result interpretation.

**Safer architecture**

The second model never needs to generate executable SQL.

**Easier iteration**

Improving the visualization/analysis prompt does not require changing the SQL-generation prompt.

---

# 🗺️ Roadmap

## Completed

- [x] Schema-grounded NL→SQL generation
- [x] SQL validation with `sqlglot`
- [x] SELECT-only enforcement
- [x] Table allowlisting
- [x] Result limits
- [x] Read-only execution path
- [x] Result-analysis LLM pass
- [x] Automatic chart-type suggestion
- [x] Evaluation harness
- [x] Semantic result comparison

## Next

- [ ] Synthetic operations dataset + seed workflow
- [ ] React analytics dashboard
- [ ] KPI cards
- [ ] Live charts
- [ ] Results table
- [ ] Conversational follow-up questions
- [ ] PostgreSQL/Neon deployment
- [ ] Production authentication
- [ ] Role-based access control
- [ ] Row-level authorization
- [ ] Column-level authorization
- [ ] Query audit logging
- [ ] Statement timeout
- [ ] Expanded evaluation benchmark

---

# 🎯 Product Direction

The long-term idea is broader than simply:

> **“AI that writes SQL.”**

The goal is to create a **natural-language decision-support layer over business databases**.

```text
                    Business question
                           │
                           ▼
                   Natural language
                           │
                           ▼
                    Data retrieval
                           │
                           ▼
                   Validated analysis
                           │
                           ▼
                  Visual explanation
                           │
                           ▼
                    Business insight
                           │
                           ▼
                       Decision
```

The Operations Analytics dataset provides a concrete starting point, but the underlying architecture can support other business domains such as:

- Sales analytics
- Customer success analytics
- Product analytics
- Finance analytics
- Supply-chain analytics
- Support analytics
- Marketing analytics

The domain changes.

The fundamental workflow remains:

> **Ask → Query → Validate → Analyze → Understand → Act**

---

# 💼 Portfolio Positioning

### Short description

> **AI-powered business analytics assistant that converts natural-language questions into safe, validated SQL and automatically transforms database results into actionable insights and visualizations.**

### Resume version

> Built an AI-powered business analytics assistant that translates natural-language business questions into validated, read-only SQL using the Claude API; implemented `sqlglot`-based SQL parsing, table allowlisting, result limits, and semantic evaluation against golden SQL queries, with a React analytics interface for tables, charts, and automated business insights.

### Technologies

```text
React
FastAPI
Python
Claude API
SQLAlchemy
PostgreSQL
SQLite
sqlglot
Recharts
Tailwind CSS
```

---

# 🎤 How to Explain It in an Interview

A strong 60-second explanation:

> “I built an AI-powered business analytics assistant for non-technical users who need answers from company data but don't know SQL. The user can ask a question in plain English, such as which warehouse has the highest order delay. The first LLM translates that question into SQL using the live database schema. I don't execute that SQL blindly — I parse it with sqlglot, enforce SELECT-only access, check referenced tables against an allowlist, and cap the result size before executing it against a read-only database. A second LLM then analyzes the returned data and recommends a suitable visualization and generates a concise business takeaway. I also built an evaluation harness with hand-verified golden queries and compare result sets rather than SQL strings, so I can measure whether the system actually answers the questions correctly.”

---

# 🔥 What Makes This Project Interesting

The project demonstrates more than calling an LLM API.

### AI Engineering

- Prompt-grounded NL→SQL generation
- Schema-aware reasoning
- Separate result-analysis model
- Structured output workflow

### Backend Engineering

- FastAPI
- SQLAlchemy
- Database integration
- API design
- Read-only execution

### Security Engineering

- SQL AST parsing
- Query allowlisting
- SELECT-only enforcement
- Result limits
- Authorization extension points

### Frontend Engineering

- React
- Interactive analytics
- Charts
- Tables
- KPI presentation

### Evaluation

- Golden SQL benchmark
- Semantic result comparison
- Repeatable accuracy measurement
- Failure inspection

---

# 🏆 Core Value Proposition

> ## **Ask the business question.**
> ## **See the data.**
> ## **Understand the insight.**
> ## **Act faster.**

The AI handles the technical translation.

The business user makes the decision.
