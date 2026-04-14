import boto3
import json
import sys


def summarize(text, model_id, region_name="us-east-1", aws_profile=None, system_prompt=""):
    """Summarize text using an AWS Bedrock model."""
    if aws_profile:
        session = boto3.Session(profile_name=aws_profile, region_name=region_name)
        bedrock = session.client("bedrock-runtime")
    else:
        bedrock = boto3.client("bedrock-runtime", region_name=region_name)

    payload = {
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": f"Transcription:\n{text}"}
        ],
        "max_tokens": 1024,
        "temperature": 0.3,
        "anthropic_version": "bedrock-2023-05-31"
    }

    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(payload)
        )
    except Exception as e:
        print(f"Error calling Bedrock: {e}", file=sys.stderr)
        return None

    result = json.loads(response["body"].read().decode())
    return "".join(
        part["text"] for part in result.get("content", [])
        if part.get("type") == "text" and "text" in part
    )
