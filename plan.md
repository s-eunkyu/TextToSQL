\## Day 1 Summary



\- Docker Desktop + WSL2 환경을 구성하고 PostgreSQL 컨테이너를 실행했다  

\- Olist 공개 이커머스 데이터를 다운로드하고 9개 CSV를 PostgreSQL(olist DB)에 적재했다  

\- 불필요한 tts DB를 정리하고 olist 중심의 실데이터 환경으로 정비했다  

\- FastAPI 서버를 구축하고 SQLAlchemy로 olist DB 연결을 완료했다  

\- /health, /db-check, /sample API를 통해 실제 customers 데이터 조회를 확인했다  

\- SQLAlchemy Inspector 기반 /tables API를 추가하여 DB 스키마 자동 조회 기반을 마련했다  

\- 프로젝트 구조를 정리하고 GitHub에 SQL 스크립트 및 API 변경 사항을 커밋했다  



결과적으로 Docker 기반 PostgreSQL에 실데이터를 구축하고, FastAPI를 통해 API → DB → 실데이터 조회까지 이어지는 Text-to-SQL 준비 단계의 백엔드 파이프라인을 완성했다.

