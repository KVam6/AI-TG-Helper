from openai import AsyncOpenAI
from openai import APITimeoutError
from config import OPENROUTER_KEY, PROMPTS

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY,
    timeout=60.0,
)

async def make_completion(requests, mode):
    try:
        completion = await client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[
                {
                    "role": "system",
                    "content": PROMPTS[mode],
                }
            ] + requests,
        )

        return completion

    except APITimeoutError:
        return None