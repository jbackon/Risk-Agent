import os
from anthropic import Anthropic

def call_llm(prompt: str) -> str:
    client = Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        base_url=os.getenv("ANTHROPIC_BASE_URL"),
    )
    message = client.messages.create(
        model="claude-sonnet-46",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}]
    )
    # print(f"[LLM] stop_reason={message.stop_reason} content={message.content}")
    return message.content[0].text
