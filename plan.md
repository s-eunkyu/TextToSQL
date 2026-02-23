최종 구조 (이번 프로젝트 1단계)

FastAPI
↓
Bedrock (LLM)
↓
SQLAlchemy
↓
PostgreSQL (로컬 Docker)
↓
FAISS (로컬)

이 구조면 이미 실무 PoC 수준입니다.

3주 실행 스케줄 (AWS 포함 버전)
1주차 핵심 목표

👉 Bedrock으로 SQL 생성 성공

Day 1

Repo 생성

Postgres docker-compose 구성

FastAPI 서버

DB 연결 테스트

Day 2

Bedrock IAM 세팅

Access Key 생성

boto3 연결 테스트

Day 3

Bedrock 호출 코드 작성

자연어 → SQL 생성 테스트

Day 4

SQL 실행 연결

자연어 → SQL → DB 실행 성공

Day 5

Guardrails 1차 구현

SELECT only

위험 키워드 차단

Day 6

질문 20개 작성

baseline 정확도 체크

2주차

스키마 문서화

FAISS 붙이기

RAG 적용

timeout + row limit

result summary

3주차

평가셋 50문항

metric 계산

README 보강

Docker 정리

아키텍처 그림
