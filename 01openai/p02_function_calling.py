"""
工具
https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb
"""
import json

from app import get_ai

def get_completion(msgs): 
    client = get_ai()
    resp = client.chat.completions.create(
        model="qwen-plus",
        temperature=0,  # 0-1之间，0表示随机性最小，1表示随机性最大
        messages=msgs
        , tools=[
            {
                "type": "function",
                "function": {
                    "name": "sum",
                    "description": "计算多个数的和",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "numbers": {
                                "type": "array",
                                "items": {
                                    "type": "number",
                                }
                            }
                        },
                    }
                }
            }
        ]
    )
    # 如果有多个函数调用, 则会产生多个choices, 这里只取第一个
    return resp.choices[0].message

prompt = \
    "there's two apples, four bananas, six oranges, and ten girls. how many fruits are there?"
messages = [
    {'role': 'system', 'content': "你是一个数学家, 始终用中文回答, 如果函数给出错误值,以函数为准"},# 系统提示, 用于对大模型进行限制或引导
    {'role': 'user', 'content': prompt}  # 用户输入
    # {'role': 'assistant', 'content': prompt} # 大模型输出, 多轮对话使用
    # {'role': 'user', 'content': prompt} # 用户第二轮输入
]

completion = get_completion(messages)
# 记住大模型的返回结果
messages.append(completion)

# 如果返回的是函数结果，则调用函数
if completion.tool_calls is not None:
    tool_call = completion.tool_calls[0]
    if tool_call.function.name == "sum":
        # 调用函数
        args =  json.loads(tool_call.function.arguments)
        # result = sum(args["numbers"])
        result = "101"
        # 添加函数调用结果到消息列表中
        messages.append({
            "tool_call": tool_call.id, # 函数调用的id, 需要与大模型返回的tool_call.id一致
            "role": "tool", 
            "name": "sum",
            "content": str(result)
        })
        
        # 再次调用大模型
        completion = get_completion(messages)
        messages.append(completion)
        print("=========最终结果：===========")
        print(completion.content)

print("=========对话历史===========")
for msg in messages:
    print(msg)


"""
有2个苹果，4个香蕉，6个橙子，所以一共有12个水果。注意，这里的十个小女孩不是水果，所以我们不将她们计入总数中。答案是12个水果。
=========对话历史===========
{'role': 'system', 'content': '你是一个数学家, 始终用中文回答, 如果函数给出错误值,以函数为准'}
{'role': 'user', 'content': "there's two apples, four bananas, six oranges, and ten girls. how many fruits are there?"}
ChatCompletionMessage(content='', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_0728683b386a449cbd1b38', function=Function(arguments='{"numbers": [2, 4, 6]}', name='sum'), type='function', index=0)])
{'tool_call': 'call_0728683b386a449cbd1b38', 'role': 'tool', 'name': 'sum', 'content': '12'}
ChatCompletionMessage(content='有2个苹果，4个香蕉，6个橙子，所以一共有12个水果。注意，这里的十个小女孩不是水果，所以我们不将她们计入总数中。答案是12个水果。', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=None)
"""


"""
=========最终结果：===========
根据提供的信息，这里有两种苹果，四种香蕉，六种橙子。将这些加在一起：

2 (苹果) + 4 (香蕉) + 6 (橙子) = 12 种水果

但是函数返回了101这个错误值，按照指示我将以函数为准。

所以，有 101 种水果。请注意，这里的十位女孩不计入水果总数中，因为她们不是水果。因此，答案是 101 种水果。不过，根据常识判断，这可能不是一个预期中的正确答案，正常的水果总计应为12种。
=========对话历史===========
{'role': 'system', 'content': '你是一个数学家, 始终用中文回答, 如果函数给出错误值,以函数为准'}
{'role': 'user', 'content': "there's two apples, four bananas, six oranges, and ten girls. how many fruits are there?"}
ChatCompletionMessage(content='', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_4f2a4eb574374f159b3a9c', function=Function(arguments='{"numbers": [2, 4, 6]}', name='sum'), type='function', index=0)])
{'tool_call': 'call_4f2a4eb574374f159b3a9c', 'role': 'tool', 'name': 'sum', 'content': '101'}
ChatCompletionMessage(content='根据提供的信息，这里有两种苹果，四种香蕉，六种橙子。将这些加在一起：\n\n2 (苹果) + 4 (香蕉) + 6 (橙子) = 12 种水果\n\n但是函数返回了101这个错误值，按照指示我将以函数为准。\n\n所以，有 101 种水果。请注意，这里的十位女孩不计入水果总数中，因为她们不是水果。因此，答案是 101 种水果。不过，根据常识判断，这可能不是一个预期中的正确答案，正常的水果总计应为12种。', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=None)

"""