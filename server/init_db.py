import os
import sys
from config.database import get_connection
from config.settings import Config
from utils.logger import get_logger

logger = get_logger("init_db")

def init_db():
    print(f"Connecting to database '{Config.DB_NAME}' at {Config.DB_HOST}:{Config.DB_PORT}...")
    
    # Path to SQL file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sql_file_path = os.path.join(base_dir, "database", "database.sql")
    
    if not os.path.exists(sql_file_path):
        print(f"Error: SQL file not found at {sql_file_path}")
        sys.exit(1)
        
    with open(sql_file_path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Split SQL file into individual statements while removing CREATE DATABASE and USE statements
    raw_statements = sql_content.split(";")
    statements = []
    for stmt in raw_statements:
        cleaned = stmt.strip()
        if not cleaned:
            continue
        # Skip CREATE DATABASE and USE statements to preserve existing cloud DB (e.g. defaultdb)
        upper_stmt = cleaned.upper()
        if upper_stmt.startswith("CREATE DATABASE") or upper_stmt.startswith("USE "):
            continue
        statements.append(cleaned)

    conn = get_connection()
    try:
        cursor = conn.cursor()
        print(f"Applying {len(statements)} SQL statements to '{Config.DB_NAME}'...")
        
        executed_count = 0
        for idx, statement in enumerate(statements, 1):
            try:
                cursor.execute(statement)
                executed_count += 1
            except Exception as e:
                print(f"Warning on statement {idx}: {e}")
                
        conn.commit()
        print(f"Successfully executed {executed_count} statements.")

        # Verify tables created
        cursor.execute("SHOW TABLES;")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"\nTables present in database '{Config.DB_NAME}':")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM `{table}`;")
            count = cursor.fetchone()[0]
            print(f"  - {table} ({count} rows)")

        cursor.close()
        print("\nDatabase initialization completed successfully!")
    except Exception as err:
        print(f"Database Initialization Error: {err}")
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
