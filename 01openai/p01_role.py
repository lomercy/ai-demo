"""
·角色：给AI定义一个最匹配任务的角色，比如：「你是一位软件工程师」「你是一位小学数学老师」
·指示：对任务进行描述
·上下文：给出与任务相关的其它背景信息（尤其在多轮交互中）
·例子：必要时给出举例，学术中称为Few-Shot Learning或In-Context Learning;对输出正确性有很大帮助
·输入：任务的输入信息；在提示词中明确的标识出输入
·输出：输出的风格、格式描述，引导只输出想要的信息，以及方便后继模块自动解析模型的输出结果，比如(JSON、XML)
"""
from app import get_ai

def get_completion(prompt , model="qwen-plus"):
    client = get_ai()
    messages=[
        # {'role': 'system', 'content': sys_content},# 系统提示, 用于对大模型进行限制或引导
        {'role': 'user', 'content': prompt} # 用户输入
        # {'role': 'assistant', 'content': prompt} # 大模型输出, 多轮对话使用
        # {'role': 'user', 'content': prompt} # 用户第二轮输入
    ]
    return client.chat.completions.create(
        model=model,
        temperature=0, # 0-1之间，0表示随机性最小，1表示随机性最大
        messages = messages
    )

target = """
你是个文笔润色大师
根据用户给出的关键字, 编造一个吸精的标题
"""

user_input = """
小米,起火
"""
prompt= f"""
# 目标
{target}
# 用户输入
{user_input}
"""

completion = get_completion(prompt)
print(completion.choices[0].message.content)
