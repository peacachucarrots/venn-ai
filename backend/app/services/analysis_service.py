# app/services/analysis_service.py
import os, openai

from .helpers.analysis_helper import describe_option
from .helpers.prompts import SYSTEM_PROMPT, USER_PROMPT
from .helpers.json_schema import JSON_SCHEMA
from ..models.response import Response

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def analyze_response(resp: Response):
    """Build a prompt, call OpenAI, return the assistant’s JSON string."""
    # bullet-format each answer
    bullets = [
        f"- {ans.question.prompt}: {describe_option(ans.option, ans.question)}"
        for ans in resp.answers
    ]

    combined_user_content = "\n".join([USER_PROMPT, *bullets])

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_schema", "json_schema": JSON_SCHEMA},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": combined_user_content},
        ]
    )

    return resp.choices[0].message.content