import boto3
import json

# Bedrock Runtime 클라이언트 생성
# Claude 호출은 bedrock-runtime 서비스로 진행
client = boto3.client(
    service_name="bedrock-runtime", # Bedrock Runtime 엔드포인트 사용
    region_name="us-east-1"         # Claude 사용 리전, 콘솔과 동일
)

# 모델 호출
response = client.invoke_model(
    modelId="anthropic.claude-3-sonnet-20240229-v1:0",  # 호출할 Claude 모델 ID
    contentType="application/json",  # 요청 바디 타입
    accept="application/json",       # 응답 타입
    body=json.dumps({                # 실제 요청 바디를 JSON 문자열로 직렬화
        "anthropic_version": "bedrock-2023-05-31",  # Claude Message API 버전
        "max_tokens": 200,                          # 응답으로 받을 수 있는 최대 토큰 수
        "messages": [
            {
                "role": "user",         # 사용자 역할
                "content": [
                    {
                        "type": "text", # 텍스트 입력
                        "text": "Reply only with: Bedrock connected successfully."
                    }
                ]
            }
        ]
    })
)

# Bedrock 응답 body는 stream 형태라 read 후 JSON 파싱이 필요
result = json.loads(response["body"].read())

# Claude 응답은 content 배열의 첫 요소에 텍스트로 존재재
print(result["content"][0]["text"])