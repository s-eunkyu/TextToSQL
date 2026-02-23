from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/olist"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-check")
def db_check():
    with engine.connect() as conn:
        row = conn.execute(text("select 1 as ok")).mappings().first()
    return {"db": "ok", "result": dict(row)}

@app.get("/sample")
def sample():
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                select customer_id, customer_city, customer_state
                from customers
                order by customer_id
                limit 20
            """)
        ).mappings().all()
    return {"rows": [dict(r) for r in rows]}