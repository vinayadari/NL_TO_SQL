import psycopg2
import config

BLOCKED_KEYWORDS = ["drop", "delete", "update", "insert", "alter", "truncate"]

def is_safe(sql):
    sql_lower = sql.lower()
    for keyword in BLOCKED_KEYWORDS:
        if keyword in sql_lower:
            return False
    return True

def run_query(sql):
    if not is_safe(sql):
        return {
            "sucess": False,
            "error": "Blocked! Query contains dangerous keywords which are not allowed"   
        }
    try:
        conn = psycopg2.connect(
            host = config.PG_HOST,
            port = config.PG_PORT,
            database = config.PG_DATABASE,
            user = config.PG_USER,
            password = config.PG_PASSWORD
        )
        
        conn.set_session(readonly = True)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        results = [dict(zip(columns, row)) for row in rows]
        results = results[:config.MCP_MAX_ROWS]
        
        cursor.close()
        conn.close()
        
        return {
            "success" : True,
            "columns" : columns,
            "rows" : results,
            "count" : len(results)
        } 
    except Exception  as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    #normal query
    print("TEST 1 - Normal query:")
    result = run_query("SELECT * FROM customers LIMIT 3")
    print(result)

    #blocked query
    print("\nTEST 2 - Blocked query:")
    result = run_query("DELETE FROM customers")
    print(result)
    