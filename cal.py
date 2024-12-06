from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # 获取请求的 JSON 数据
        data = request.get_json()
        operand1 = data['operand1']
        operand2 = data['operand2']
        operator = data['operator']
        
        # 执行相应的计算
        if operator == '+':
            result = operand1 + operand2
        elif operator == '-':
            result = operand1 - operand2
        elif operator == '*':
            result = operand1 * operand2
        elif operator == '/':
            result = operand1 / operand2
        else:
            return jsonify({"error": "Invalid operator"}), 400
        
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8641)
