import psycopg2
import config
from collections import defaultdict


def get_schema():
    try:
        conn = psycopg2.connect(
            host = config.PG_HOST,
            port = config.PG_PORT,
            database = config.PG_DATABASE,
            user = config.PG_USER,
            password = config.PG_PASSWORD
        )

        cursor = conn.cursor()

        cursor.execute("""
                    SELECT table_name, column_name, data_type
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    ORDER BY table_name, ordinal_position;
        """)#fetch all the meta data stored in psql default

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        schema = defaultdict(list)

        for table, column, dtype in rows:
            schema[table].append(f"{column}({dtype})")
                
        schema_str = ""
        for table, columns in schema.items():
            schema_str += f"{table}({','.join(columns)})\n"
            
            
        return schema_str.strip()
    except Exception as e:
        return f"Error loading schema: {e}"


if __name__ == "__main__":
    print(get_schema())
    
    
## The full flow
# ```
# PostgreSQL DB
#      ↓
# information_schema.columns  ← built-in metadata table
#      ↓
# Python dictionary  ← grouped by table
#      ↓
# Formatted string  ← ready for LLM prompt
        


        
