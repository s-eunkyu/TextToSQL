# 테이블을 순회하면서 스키마를 읽고 Claude에게 문서화를 맡겨서 schemas 폴더에 md를 생성합니다.

import json
from pathlib import Path
from bedrock_client import call_claude      # Claude 호출 함수
from schema_loader import get_schema로      # 스키마 로더 함수

# 1. 대상 테이블 목록 정의
tables = [
    "customers", "orders", "order_items", "products",
    "payments", "reviews", "sellers", "geolocation", "category_translation"
]

# 2. 결과 저장할 schemas 폴더 준비
output_dir = Path("schemas")
output_dir.mkdir(exist_ok=True)

# 3. 테이블별로 문서 생성
for table in tables:
    # 4. DB에서 테이블 스키마 가져오기
    schema = get_schema(table)

    # 5. prompt에 스키마를 JSON으로 포함
    #   - Claude에 전달할 프롬프트 구성
    prompt = f"""
You are a senior data analyst documenting a PostgreSQL database.

Given this table schema:

{json.dumps(schema, indent=2)}

Write:

1. What this table represents
2. Explanation of each column
3. Typical joins with other tables
4. Example business questions
"""

    # 진행 상황 출력
    print(f"Generating {table}...")

    # 6. Claude 호출해서 문서 생성
    doc = call_claude(prompt)

    # 7. md 파일로 저장 (ex. schemas/orders.md)
    with open(output_dir / f"{table}.md", "w", encoding="utf-8") as f:
        f.write(f"# {table}\n\n")   # md 제목
        f.write(doc)                # Claude 생성 본문

# 전체 완료 출력
print("Done.")