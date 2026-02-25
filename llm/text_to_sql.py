# llm/text_to_sql.py
import json
import boto3

client = boto3.client("bedrock-runtime", region_name="us-east-1")

def generate_sql_with_claude(question: str, schema_context: str) -> str:
    system_prompt = (
        "You are a senior data analyst. "
        "Generate a single SQL query for PostgreSQL. "
        "Return SQL only. No explanation. No markdown."
    )

    user_prompt = (
        "Schema context:\n"
        f"{schema_context}\n\n"
        "User question:\n"
        f"{question}\n\n"
        "SQL:"
    )

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "system": system_prompt,          # ✅ 여기로 이동
        "max_tokens": 400,
        "temperature": 0.0,
        "messages": [
            {"role": "user", "content": user_prompt},   # ✅ system role 제거
        ],
    }

    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"  # 또는 haiku

    resp = client.invoke_model(
        modelId=model_id,
        body=json.dumps(body),
        accept="application/json",
        contentType="application/json",
    )

    out = json.loads(resp["body"].read())
    text = out["content"][0]["text"].strip()

    return text.strip().strip("```").strip()