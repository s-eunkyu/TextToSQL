# PostgreSQL에서 테이블 컬럼 메타데이터를 가져와, LLM에게 줄 스키마 JSON을 만듭니다.

from sqlalchemy import create_engine, inspect

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/olist"

# SQLAlchemy 엔진 생성, 실제 커넥션은 필요 시 생성됨
engine = create_engine(DATABASE_URL)

# 테이블, 컬럼, 인덱스, 외래키 같은 메타데이터를 읽는 객체
inspector = inspect(engine)

def get_schema(table: str):
    # 특정 테이블의 컬럼 메타데이터 조회
    columns = inspector.get_columns(table)

    # LLM에게 주기 좋은 형태로 정리
    return {
        "table": table,
        "columns": [
            {
                "name": col["name"],
                "type": str(col["type"])
            }
            for col in columns
        ]
    }