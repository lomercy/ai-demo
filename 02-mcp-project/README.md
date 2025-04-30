# 环境准备

安装uv
```python
pip install uv
```

创建项目
```python
uv init 02-mcp-project
```

创建.env文件, 输入以下内容
```markdown
BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL=qwen2.5-vl-32b-instruct
DASHSCOPE_API_KEY="xxxx"

SERPER_API_KEY="xxx"
SMTP_SERVER=smtp.qq.com
SMTP_PORT=465
EMAIL_USER=bootystar@qq.com
EMAIL_PASS=xxxx
```