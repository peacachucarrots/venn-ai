# app/services/analysis_service.py
import os, openai

from .helpers.analysis_helper import describe_option
from .helpers.prompts import system_prompt, user_prompt
from ..models.response import Response

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def analyze_response(resp: Response):
    """Build a prompt, call OpenAI, return the assistant’s JSON string."""
    # bullet-format each answer
    bullets = [
        f"- {ans.question.prompt}: {describe_option(ans.option, ans.question)}"
        for ans in resp.answers
    ]

    system_content = system_prompt
    user_content = "\n".join([user_prompt, *bullets])

    completion = client.chat.completions.create(
        model="o3",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ]
    )
    return completion.choices[0].message.content, user_content