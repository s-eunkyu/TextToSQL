# Bedrock Titan Embeddings V2로 텍스트를 임베딩 벡터로 변환하는 함수 제공

import boto3
import json
from typing import List

# Bedrock Runtime 클라이언트 생성
_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

# 역할: 입력 텍스트를 임베딩 벡터로 변환
def embed_text(text: str, dimensions: int = 1024, normalize: bool = True) -> List[float]:
    # text: 임베딩할 원문 텍스트
    # dimensions: 임베딩 차원 수, Titan v2는 1024를 기본으로 사용
    # normalize: True면 벡터를 정규화하여 내적 검색이 코사인 유사도처럼 동작하도록 도움

    # Titan Embeddings 요청 바디 구성
    body = {
        "inputText": text,          # 임베딩 텍스트
        "dimensions": dimensions,   # 출력 벡터 차원 수
        "normalize": normalize      # 벡터 정규화 여부
    }

    # Bedrock invoke_model 호출
    resp = _client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0", # Titan Embeddings V2 모델
        contentType="application/json",     # 요청 타입
        accept="application/json",          # 응답 타입
        body=json.dumps(body)               # dict -> JSON 문자열
    )

    data = json.loads(resp["body"].read())

    # 임베딩한 결과 반환
    return data["embedding"]