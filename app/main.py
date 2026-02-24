from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError

# FastAPI 앱 생성 (uvicorn이 실행하는 app 객체)
app = FastAPI(title="Text-to-SQL (Olist)")

# PostgreSQL 연결 설정 (olist 데이터베이스 사용)
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/olist"

# SQLAlchemy 엔진 생성
# pool_pre_ping=True: 연결이 끊어져도 자동으로 다시 연결하는 기능
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


# =========================================================
# 1) 테이블 목록 조회 API
# =========================================================
# olist DB에 어떤 테이블들이 있는지 반환
# Text-to-SQL에서 '어떤 테이블이 존재하는지' 알려주는 역할
@app.get("/tables")
def list_tables():
    inspector = inspect(engine) # DB 메타데이터 접근 객체
    return {"tables": inspector.get_table_names()} # 테이블 이름 리스트 반환


# =========================================================
# 2) 테이블 스키마 조회 API
# =========================================================
# 컬럼 이름 / 타입 / nullable 여부 반환
# RAG에서 LLM에게 넘길 핵심 정보
@app.get("/schema/{table_name}")
def get_table_schema(table_name: str):
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    # 존재하지 않는 테이블 요청 시 404 에러 반환
    if table_name not in tables:
        raise HTTPException(status_code=404, detail=f"Table {table_name} not found")

    # 컬럼 메타데이터 조회
    columns = inspector.get_columns(table_name)

    # 필요한 정보만 정리
    result = [
        {
            "name": c["name"],          # 컬럼 이름
            "type": str(c["type"]),     # 컬럼 타입
            "nullable": c["nullable"]   # NULL 허용 여부
        } for c in columns
    ]

    return {"table": table_name, "columns": result}


# =========================================================
# 3) SQL 실행 API (SELECT 쿼리 전용)
# =========================================================
# 나중에 Bedrock에서 생성한 SQL 쿼리를 실행하는 역할
class QueryRequest(BaseModel):
    sql: str         # 실행할 SQL 쿼리
    limit: int = 100 # 조회 결과 개수 제한 (기본값: 100)

# 위험한 키워드 차단 (LLM 사고 방지용)
BLOCKED_KEYWORDS = [
    "drop", "truncate", "alter", "create",
    "insert", "update", "delete",
    "grant", "revoke", "rename"
]

# SELECT 문인지 + 위험 키워드 없는지 체크
def is_safe_select(sql: str) -> bool:
    s = sql.strip().lower()

    # SELECT로 시작하지 않으면 거부
    if not s.startswith("select"):
        return False

    # 위험 키워드 포함 시 거부
    for kw in BLOCKED_KEYWORDS:
        if kw in s:
            return False
    
    return True


@app.post("/query")
def run_query(req: QueryRequest):
    sql = req.sql.strip().rstrip(";") # 세미콜론 제거

    # SELECT만 허용
    if not is_safe_select(sql):
        raise HTTPException(status_code=400, detail="Only SELECT queries are allowed")

    # LIMIT 없으면 강제 추가 (초반 안전장치)
    if "limit" not in sql.lower():
        sql = f"{sql} LIMIT {int(req.limit)}"
    
    try:
        # SQL 실행
        with engine.connect() as conn:
            rows = conn.execute(text(sql)).mappings().all()

        # 결과 반환
        return {
            "sql": sql,
            "row_count": len(rows),
            "rows": [dict(r) for r in rows]
        }

    except SQLAlchemyError as e:
        # DB 에러 발생 시 500 반환
        raise HTTPException(status_code=500, detail=f"DB error: {e}")