from openai import AsyncOpenAI  

from config import OPENROUTER_KEY, PROMPTS

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY,
)

async def make_completion(request: str, mode: str):
    completion = await client.chat.completions.create(
        model='openai/gpt-oss-120b:free',
        messages=[
            {"role": "system", "content" : PROMPTS[mode]},
            {"role": "user", "content": request}
        ]
    )
    return completion