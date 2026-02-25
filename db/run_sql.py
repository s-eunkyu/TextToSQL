# db/run_sql.py
import os
import psycopg2

def run_sql(sql: str):
    conn = psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=int(os.getenv("PGPORT", "5432")),
        dbname=os.getenv("PGDATABASE", "olist"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "postgres"),
    )
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            if cur.description is None:
                return [], []
            columns = [d.name for d in cur.description]
            rows = cur.fetchall()
            return rows, columns
    finally:
        conn.close()