# rag/build_faiss.py
# 역할: schemas 폴더의 md 문서를 읽어 chunk로 분할하고
#       Bedrock 임베딩을 생성한 뒤 FAISS 인덱스와 메타데이터를 파일로 저장

import json
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
import faiss             # 벡터 검색 인덱스

from embeddings_bedrock import embed_text  # Bedrock 임베딩 함수

# 입력 문서 폴더
SCHEMAS_DIR = Path("schemas")

# 출력 폴더 및 파일 경로
OUT_DIR = Path("rag")
OUT_DIR.mkdir(exist_ok=True)

INDEX_PATH = OUT_DIR / "schema.index"       # FAISS 인덱스 파일
META_PATH = OUT_DIR / "schema_meta.jsonl"   # chunk별 메타데이터 저장 파일 jsonl

def split_markdown(md: str, max_chars: int = 1200) -> List[str]:
    # 역할: Markdown 문서를 너무 길지 않게 chunk로 나눔
    # 전략:
    # 1 헤더를 만나면 끊기
    # 2 max_chars를 넘으면 끊기
    # 이유:
    # - 너무 짧으면 문맥이 약해지고
    # - 너무 길면 임베딩이 뭉개질 수 있음

    parts: List[str] = []   # 최종 chunk 리스트
    buf: List[str] = []     # 현재 chunk를 쌓는 버퍼
    size = 0                # 현재 버퍼의 글자 수

    for line in md.splitlines():  # 한 줄씩 처리
        # 헤더를 만나면 chunk를 분리
        if line.startswith("#") and buf:
            parts.append("\n".join(buf).strip())
            buf, size = [], 0

        # 버퍼에 현재 줄 추가
        buf.append(line)
        size += len(line) + 1

        # 길이가 max_chars 이상이면 chunk를 분리
        if size >= max_chars:
            parts.append("\n".join(buf).strip())
            buf, size = [], 0

    # 마지막 남은 버퍼 처리
    if buf:
        parts.append("\n".join(buf).strip())

    # 공백 chunk 제거
    return [p for p in parts if p]

def main() -> None:
    # schemas 폴더에서 md 파일 목록 가져오기
    md_files = sorted(SCHEMAS_DIR.glob("*.md"))
    if not md_files:
        raise RuntimeError("schemas 폴더에 md 파일이 없습니다. 먼저 md 생성부터 해주세요.")

    chunks: List[Dict[str, Any]] = []    # 각 chunk의 metadata 및 원문 저장
    vectors: List[List[float]] = []      # 각 chunk의 임베딩 벡터 저장

    for fp in md_files:
        table = fp.stem                               # 파일명에서 테이블명 추출
        md = fp.read_text(encoding="utf-8")           # md 본문 읽기

        # md를 chunk로 분할
        for i, chunk in enumerate(split_markdown(md)):
            # 검색 안정화를 위해 table 힌트를 살짝 붙여 임베딩합니다
            # 질문에 table명이 직접 나오지 않아도 매칭이 잘 되는 편입니다
            text_for_embed = f"table: {table}\n\n{chunk}"

            # Bedrock 임베딩 생성
            vec = embed_text(text_for_embed)

            # 저장
            vectors.append(vec)
            chunks.append({
                "id": len(chunks),        # 전역 chunk id
                "table": table,           # 어떤 테이블 md에서 왔는지
                "chunk_index": i,         # 해당 md 내 chunk 번호
                "text": chunk             # chunk 원문, 나중에 프롬프트 컨텍스트로 사용
            })

        print(f"Embedded {table}")

    # FAISS는 float32 ndarray를 선호합니다
    mat = np.array(vectors, dtype="float32")

    # 임베딩 차원
    dim = mat.shape[1]

    # IndexFlatIP: Inner Product 기반 인덱스
    # normalize=True로 임베딩했다면 코사인 유사도와 유사하게 동작합니다
    index = faiss.IndexFlatIP(dim)

    # 벡터 추가
    index.add(mat)

    # 인덱스 파일 저장
    faiss.write_index(index, str(INDEX_PATH))

    # 메타데이터는 jsonl로 저장
    # 각 줄이 하나의 JSON 객체이므로, 로딩이 간단합니다
    with open(META_PATH, "w", encoding="utf-8") as f:
        for row in chunks:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"OK - chunks: {len(chunks)}")
    print(f"Saved index: {INDEX_PATH}")
    print(f"Saved meta : {META_PATH}")

if __name__ == "__main__":
    main()