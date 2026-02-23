# TextToSQL

Natural language to SQL service with RAG and guardrails using FastAPI

</br>

# Text to SQL with RAG and Guardrails

자연어 질문을 SQL로 변환해 실제 데이터베이스에 실행하고, 결과를 반환하는 개인 포트폴리오 프로젝트입니다.  
스키마 기반 RAG를 통해 정확도를 높이고, SQL Guardrails로 위험 쿼리를 차단합니다.

단순 모델 실험이 아닌,

- Retrieval  
- Validation  
- Execution  
- Evaluation  

까지 포함한 end to end Text to SQL 파이프라인 구현을 목표로 했습니다.

---

## 프로젝트 목적

- 자연어 기반 데이터 조회 경험 구현  
- 스키마 검색 기반 RAG 구조 이해  
- SQL 안전 검증 로직 설계  
- 실제 DB 실행 + 결과 요약  
- 정량 평가 파이프라인 구축  

---

## 주요 기능

- Natural Language to SQL  
- Schema Retrieval with RAG  
- SQL Guardrails  
  - SELECT only  
  - 위험 키워드 차단  
  - 다중 statement 차단  
  - row limit 적용  
  - timeout 적용  
- Query Execution  
- Result Summarization  
- Evaluation Pipeline  

---

## 전체 흐름

1. 사용자 자연어 질문 입력  
2. 스키마 문서 벡터 검색  
3. 검색 결과 + 질문을 LLM에 전달  
4. SQL 생성  
5. Guardrails 검증  
6. DB 실행  
7. 결과 및 요약 반환  

---

## 기술 스택

- API: FastAPI  
- Database: PostgreSQL 또는 SQLite  
- Vector Store: FAISS  
- LLM: 선택 모델 1종  
- Evaluation: Python  

---

## 프로젝트 구조

app/
  main.py  
  api/  
  core/  
  services/  

data/
  sample_db/  
  schema_docs/  

scripts/
  build_docs.py  
  ingest_vectors.py  

eval/
  dataset.csv  
  run_eval.py  

docker/  
README.md  

---

## 실행 방법

### 1. 가상환경 생성

python -m venv .venv  
source .venv/bin/activate  

윈도우

.venv\Scripts\activate  

---

### 2. 패키지 설치

pip install -r requirements.txt  

---

### 3. 환경 변수 설정

LLM_PROVIDER=bedrock or openai  
DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/db  
VECTOR_STORE=faiss  
TOP_K=5  
MAX_ROWS=200  
QUERY_TIMEOUT_SEC=10  

---

### 4. 스키마 문서 생성 및 벡터 적재

python scripts/build_docs.py  
python scripts/ingest_vectors.py  

---

### 5. 서버 실행

uvicorn app.main:app --reload  

---

## API

### GET /health

서버 상태 확인  

---

### GET /schema

현재 연결된 DB의 테이블 및 컬럼 요약 반환  

---

### POST /query

Request

{
  "question": "최근 30일 매출 상위 고객 10명"
}

Response

- generated SQL  
- query result rows  
- short summary  
- retrieval metadata  

---

## SQL Guardrails

- SELECT 문만 허용  
- DROP DELETE UPDATE INSERT ALTER TRUNCATE 차단  
- 세미콜론 기반 다중 쿼리 차단  
- 결과 row 제한  
- 실행 시간 제한  

---

## Evaluation

### Dataset

eval/dataset.csv  

- question  
- gold_sql  
- tags  

---

### 평가 실행

python eval/run_eval.py  

---

### Metrics

- execution_success_rate  
- result_match_rate  
- blocked_rate  
- avg_latency_ms  

---

## 향후 개선 계획

- multi schema 지원  
- SQL AST 기반 검증  
- self correction loop  
- retrieval caching  
- role based access control  

---

## License

MIT
