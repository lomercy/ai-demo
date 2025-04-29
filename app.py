
def get_ai():
    import os
    from openai import OpenAI
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"), # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    return client


# def get_completion(user_content , sys_content , model="qwen-plus"):
#     client = get_ai()
#     messages=[
#         {'role': 'system', 'content': sys_content},
#         {'role': 'user', 'content': user_content}
#     ]
#     completion = client.chat.completions.create(
#         model=model,
#         messages = messages
#         # temperature=0.7, # 生成结果的多样性, 取值0-2, 越大越发散
#         # seed=123, # 随机种子, 指定后, 当temperature=0时, 结果是固定的
#         # stream=false # 数据流格式, 是否一个一个字输出
#         # response_format={"type": "json_object"} # 输出格式, 默认为text, 可选值有：text, json_object, xml
#         # max_tokens=1000 # 输出的最大token数, 默认为无穷大
#         # presence= 0 # 对出现过的token进行降权
#         # logit_bias= 0 # 对token采样进行加,降权
#     )
#     return completion
# 
# 
# def get_completion_str(user_content , sys_content = "your name is bootystar's ai assist", model="qwen-plus"):
#     return get_completion(user_content,sys_content).choices[0].message.content



