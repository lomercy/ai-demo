"""
仅gpt-4支持
国内模型暂不支持
"""
from openai import OpenAI
from pydantic import BaseModel



class Step(BaseModel):
    explanation: str
    output: str


class MathResponse(BaseModel):
    steps: list[Step]
    final_answer: str


client = OpenAI()
completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06", # 仅在此之上的模型支持
    messages=[
        {"role": "system", "content": "You are a helpful math tutor."},
        {"role": "user", "content": "solve 8x + 31 = 2"},
    ],
    response_format=MathResponse,
)

message = completion.choices[0].message
print(message)
print("============")
if message.parsed:
    print(message.parsed.steps)
    print("answer: ", message.parsed.final_answer)