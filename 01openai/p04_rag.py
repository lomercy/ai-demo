"""
配合向量储存, 提取知识库内容, 并给ai提供上下文, 让ai回答问题

安装检索引擎
pip install elasticsearch7
pip install nltk

运行环境

docker pull docker.elastic.co/elasticsearch/elasticsearch:9.0.0
docker run -d --name es01  -p 9200:9200 -p 9300:9300  -m 1GB docker.elastic.co/elasticsearch/elasticsearch:9.0.0

# 获取密码, 默认账号elastic
docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic

# 获取kibana token, 默认账号kibana
docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana

docker pull docker.elastic.co/kibana/kibana:9.0.0
docker run -d --name kib01 -p 5601:5601 docker.elastic.co/kibana/kibana:9.0.0

# 密码
eAMoLrpHCNK0dqzO5c3S

# kibana token
eyJ2ZXIiOiI4LjE0LjAiLCJhZHIiOlsiMTcyLjE3LjAuMjo5MjAwIl0sImZnciI6IjY4YTAyMzdiZDE1OWI4NmYyYjJiYjllNWM2ZWVlN2ZmOTA3MDMxZjBlNTkzZmFkMmE1NjU0OGE0MTJlOGQ4MjIiLCJrZXkiOiJhenl5Z0pZQlNGREROTkVTYlkwYTpoMFNILWpvM3kwd0Q4cFluczBkMEdBIn0=
"""
from app import get_ai



# 根据模板生成prompt, 其中**kwargs是一个字典, 用于替换模板中的变量
def get_prompt(prompt_template, **kwargs):
    inputs = {}
    for k,v in kwargs.items():
        if isinstance(v,list) and all(isinstance(elem,str) for elem in v):
            val = "\n\n".join(v)
        else:
            val = v
        inputs[k] = val
    return prompt_template.format(**inputs)

# 已知信息
context="""
周一上课
周三上课
"""
# 问题
question="你是谁"

template=f"""
根据以下已知信息, 回答用户问题

已知信息：
{context}

用户问题：
{question}

如果无法从中得到答案, 请说 "根据已知信息无法回答该问题" 或 "没有提供足够的相关信息"，不允许在答案中添加编造成分，答案请使用中文回答。
"""


client = get_ai()
messages=[
    {'role': 'user', 'content': template}
]
# messages=get_prompt(template,context=context,question=question)
completion = client.chat.completions.create(
    model="qwen-plus", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages
)

resp= completion.choices[0].message.content
messages.append(resp)

for message in messages:
    print(message)
