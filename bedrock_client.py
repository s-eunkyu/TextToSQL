import boto3
import json

# Bedrock Runtime 클라이언트 자주 쓰이므로 모듈 로드 시 1회 생성
client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

# Claude 호출 로직 함수
def call_claude(prompt: str, max_tokens=1000,  model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0") -> str:
    # prompt: Claude에게 보낼 텍스트 프롬프트
    # max_tokens: 응답 길이 제한
    # model_id: 사용할 모델, 필요하다면 haiku로 바꿔 비용 절감 가능

    # invoke_model 호출
    response = client.invoke_model(
        modelId=model_id,                 # 호출할 모델 ID
        contentType="application/json",   # 요청 타입
        accept="application/json",        # 바디 타입
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",  # Claude 메시지 API 버전
            "max_tokens": max_tokens,     # 응답 토큰 제한
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt # 실제 입력 텍스트
                        }
                    ]
                }
            ]
        })
    )

    # 응답 바디는 stream이라 read 후 JSON 파싱
    result = json.loads(response["body"].read())

    # Claude 응답 텍스트 반환
    return result["content"][0]["text"]