from zhipuai import ZhipuAI
import json
import requests

# 定义计算器函数的工具描述
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "A calculator that performs arithmetic operations (+, -, *, /)",
            "parameters": {
                "type": "object",
                "properties": {
                    "operand1": {
                        "description": "The first operand (number).",
                        "type": "number"
                    },
                    "operand2": {
                        "description": "The second operand (number).",
                        "type": "number"
                    },
                    "operator": {
                        "description": "The operator (+, -, *, /).",
                        "type": "string"
                    }
                },
                "required": ["operand1", "operand2", "operator"]
            }
        }
    }
]


client = ZhipuAI(api_key="de081fb1e13619e6d979ae271042eac5.a8whmZ0FG24RRPDF")  
# 初始化消息
messages = [{"role": "user", "content": f"我想知道129032910921*188231"}]

# 调用模型
response = client.chat.completions.create(
    model="glm-4",  # 使用适当的模型名称
    messages=messages,
    tools=tools,
)

print(response.choices[0].message.tool_calls[0].function.arguments)

tool_calls = response.choices[0].message.tool_calls

arguments = tool_calls[0].function.arguments
if isinstance(arguments, str):
    arguments = json.loads(arguments)  # 将 JSON 字符串转换为字典
    print("Parsed arguments:", arguments)  # 打印解析后的字典

# 提取并打印 operand1 和 operand2
operand1 = arguments.get('operand1')
operand2 = arguments.get('operand2')
print(f"operand1: {operand1}, operand2: {operand2}")

# 调用计算器API接口
api_url = "http://127.0.0.1:8641/calculate"  # 计算器API
data = {
    'operand1': operand1,
    'operand2': operand2,
    'operator': arguments.get('operator')  # 获取 operator
}

# 发起POST请求
try:
    api_response = requests.post(api_url, json=data)
    api_response.raise_for_status()  # 检查请求是否成功
    result = api_response.json()  # 解析JSON响应
    print(f"Calculation result from API: {result['result']}")
    messages.append({
        "role": "tool",
        "content": f"{json.dumps(result)}",
        "tool_call_id": tool_calls[0].id
    })
    response = client.chat.completions.create(
        model="glm-4",  
        messages=messages,
        tools=tools,
    )
    # 打印模型响应
    print(response.choices[0].message.content)
except requests.exceptions.RequestException as e:
    print(f"Error calling calculator API: {e}")
