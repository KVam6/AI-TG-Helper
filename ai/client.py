from openai import OpenAI

from config import OPENROUTER_KEY

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY,
)

completion = client.chat.completions.create(
model='openai/gpt-oss-120b:free', 
messages=[
    {
        "role": "user",
        "content": "Передай привет всему миру, how are u"
    }
]
)
#print(completion.choices[0].message.content)
