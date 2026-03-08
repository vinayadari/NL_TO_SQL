import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
from nl_to_sql import nl_to_sql
from db_executor import run_query
from schema_loader import get_schema


# Initialize MCP server
app = Server("nl2sql-mcp")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """Register all available MCP tools"""
    return [
        types.Tool(
            name="ask_database",
            description="Convert a natural language question to SQL and run it on PostgreSQL",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Natural language question about the database"
                    }
                },
                "required": ["question"]
            }
        ),
        types.Tool(
            name="run_sql",
            description="Run a raw SQL SELECT query directly on PostgreSQL",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "A valid PostgreSQL SELECT query"
                    }
                },
                "required": ["sql"]
            }
        ),
        types.Tool(
            name="get_schema",
            description="Get the full database schema — all tables and columns",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls from MCP clients"""

    # ── Tool 1: ask_database ──
    if name == "ask_database":
        question = arguments.get("question", "")

        if not question:
            return [types.TextContent(
                type="text",
                text=json.dumps({"error": "No question provided"})
            )]

        # Convert to SQL
        sql, error = nl_to_sql(question)

        if error:
            return [types.TextContent(
                type="text",
                text=json.dumps({"error": error})
            )]

        # Run SQL
        result = run_query(sql)
        result["sql_generated"] = sql

        return [types.TextContent(
            type="text",
            text=json.dumps(result, default=str)
        )]

    # ── Tool 2: run_sql ──
    elif name == "run_sql":
        sql = arguments.get("sql", "")

        if not sql:
            return [types.TextContent(
                type="text",
                text=json.dumps({"error": "No SQL provided"})
            )]

        result = run_query(sql)

        return [types.TextContent(
            type="text",
            text=json.dumps(result, default=str)
        )]

    # ── Tool 3: get_schema ──
    elif name == "get_schema":
        schema = get_schema()
        return [types.TextContent(
            type="text",
            text=json.dumps({"schema": schema})
        )]

    else:
        return [types.TextContent(
            type="text",
            text=json.dumps({"error": f"Unknown tool: {name}"})
        )]


async def main():
    print("🚀 NL2SQL MCP Server starting...")
    print("📡 Listening for MCP client connections via stdio")
    print("🛠️  Tools: ask_database | run_sql | get_schema")

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())