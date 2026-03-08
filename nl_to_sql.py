import ollama 
import config
from schema_loader import get_schema

def nl_to_sql(question):
    schema = get_schema()
    prompt = f"""You are a PostgreSQL expert. Convert the question below to SQL.
            DATABASE SCHEMA:
            {schema}

            QUESTION: {question}

            STRICT RULES:
            - Return ONLY the SQL query, nothing else
            - No explanations, no markdown, no code blocks
            - Only SELECT statements
            - Match the question EXACTLY — do not answer a different question
            - End with semicolon

            EXAMPLES:
            Question: Show me customers from California
            SQL: SELECT * FROM customers WHERE state = 'CA';

            Question: How many orders were delivered?
            SQL: SELECT COUNT(*) FROM orders WHERE status = 'delivered';

            Question: Top 5 most expensive products?
            SQL: SELECT product_name, price FROM products ORDER BY price DESC LIMIT 5;

            Now convert this question:
            Question: {question}
            SQL:"""
    
    response = ollama.chat(
        model=config.OLLAMA_MODEL,
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )
    
    sql = response["message"]["content"].strip()
    
    sql = sql.replace("```sql", "").replace("```", "").strip()
    
    if not sql.lower().startswith("select"):
        return None, "LLM returned a non-SELECT query — blocked!"
    
    return sql, None

def clear_history():
    """Reset conversation history"""
    global conversation_history
    conversation_history = []
    print("✅ Conversation history cleared.")
if __name__ == "__main__":
    questions = [
        "Show me all premium customers",
        "How many orders were delivered?",
        "What are the top 5 most expensive products?"
    ]
    
    for q in questions:
        print(f"\nQuestion: {q}")
        sql, error = nl_to_sql(q)
        if error:
            print(f"Error: {error}")
        else:
            print(f"SQL: {sql}")
    
    print("enter you're query: ", end="")
    query = input()
    while query != "q":
        sql, error = nl_to_sql(q)
        if error:
            print(f"Error: {error}")
        else:
            print(f"SQL: {sql}")
        print("enter you're query: ", end="")
        query = input()
    print("end of the queries")

