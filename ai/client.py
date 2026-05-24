from openai import AsyncOpenAI  

from config import OPENROUTER_KEY

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY,
)

async def make_completion(request: str):
    completion = await client.chat.completions.create(
        model='openai/gpt-oss-120b:free', 
        messages=[{"role": "user", "content": request}]
    )
    return completion