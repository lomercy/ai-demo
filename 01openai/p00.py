"""

"""
from app import get_ai

client = get_ai()
messages=[
    {'role': 'system', 'content': '''
        You are a teacher. to tell user when the class is started , there\'s only on monday and tuesday has class
        '''},
    {'role': 'user', 'content': '''
        今天上课不？
        '''}
]
completion = client.chat.completions.create(
    model="qwen-plus", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages
)

resp= completion.choices[0].message.content
messages.append(resp)

for message in messages:
    print(message)
