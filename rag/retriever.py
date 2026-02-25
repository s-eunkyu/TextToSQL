# rag/retriever.py
# 역할: FAISS 인덱스와 메타데이터를 로드하고
#       사용자의 질의 텍스트에 대해 top_k 관련 chunk를 반환

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

import numpy as np
import faiss

from rag.embeddings_bedrock import embed_text  # 질문 임베딩 생성

# 저장된 인덱스와 메타 파일 경로
OUT_DIR = Path("rag")
INDEX_PATH = OUT_DIR / "schema.index"
META_PATH = OUT_DIR / "schema_meta.jsonl"

def _load_meta() -> List[Dict[str, Any]]:
    # 역할: jsonl 메타파일을 리스트로 로드
    rows: List[Dict[str, Any]] = []
    with open(META_PATH, "r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    return rows

# 간단한 캐시
_index_cache: Optional[faiss.Index] = None
_meta_cache: Optional[List[Dict[str, Any]]] = None

def retrieve(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    # 역할: query를 임베딩하고 FAISS에서 top_k 유사 chunk 검색
    # 반환: [{"score":..., "table":..., "chunk_index":..., "text":...}, ...]

    global _index_cache, _meta_cache

    # 인덱스 로드 1회
    if _index_cache is None:
        if not INDEX_PATH.exists():
            raise RuntimeError("FAISS 인덱스가 없습니다. 먼저 python -m rag.build_faiss 실행하세요.")
        _index_cache = faiss.read_index(str(INDEX_PATH))

    # 메타 로드 1회
    if _meta_cache is None:
        if not META_PATH.exists():
            raise RuntimeError("메타데이터 파일이 없습니다. 먼저 python -m rag.build_faiss 실행하세요.")
        _meta_cache = _load_meta()

    # 질의 임베딩 생성
    qvec = embed_text(query)

    # FAISS 입력 형태는 (n, dim) 형태의 float32 배열이어야 합니다
    qmat = np.array([qvec], dtype="float32")

    # 검색 수행
    scores, ids = _index_cache.search(qmat, top_k)

    # 결과 매핑
    results: List[Dict[str, Any]] = []
    for score, idx in zip(scores[0].tolist(), ids[0].tolist()):
        # FAISS가 -1을 주는 경우가 있을 수 있어 방어
        if idx < 0:
            continue

        row = _meta_cache[idx]
        results.append({
            "score": float(score),         # 유사도 점수 (Inner Product)
            "table": row["table"],         # 테이블명
            "chunk_index": row["chunk_index"],
            "text": row["text"]            # Claude 프롬프트 컨텍스트로 넣을 텍스트
        })

    return results