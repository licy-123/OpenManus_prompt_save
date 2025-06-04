from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import json
import random  # 用于模拟检测结果

app = Flask(__name__)
CORS(app)

# 数据库初始化
def init_db():
    conn = sqlite3.connect('security.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            result TEXT NOT NULL,
            level TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def check_prompt(prompt):
    # 防御级别1的关键词
    defense1_keywords = [
        '违法', '犯罪', '暴力', '色情', '赌博', '毒品',
        '自杀', '自残', '虐待', '歧视', '仇恨'
    ]
    
    # 防御级别2的关键词
    defense2_keywords = [
        '敏感', '政治', '宗教', '种族', '性别',
        '隐私', '机密', '密码', '账号', '个人信息'
    ]
    
    # 检查防御级别1
    for keyword in defense1_keywords:
        if keyword in prompt:
            return {
                'status': 'defense1',
                'content': None
            }
    
    # 检查防御级别2
    for keyword in defense2_keywords:
        if keyword in prompt:
            return {
                'status': 'defense2',
                'content': None
            }
    
    # 安全内容
    return {
        'status': 'safe',
        'content': prompt
    }

@app.route('/api/check', methods=['POST'])
def check():
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'error': '提示词不能为空'}), 400
    
    result = check_prompt(prompt)
    return jsonify(result)

@app.get("/api/history.php")
async def get_history():
    conn = sqlite3.connect('security.db')
    c = conn.cursor()
    c.execute("SELECT timestamp, prompt, result FROM history ORDER BY timestamp DESC LIMIT 10")
    records = c.fetchall()
    
    return [
        {
            "time": record[0],
            "prompt": record[1],
            "result": record[2]
        }
        for record in records
    ]

@app.get("/api/statistics.php")
async def get_statistics():
    conn = sqlite3.connect('security.db')
    c = conn.cursor()
    c.execute("SELECT level, COUNT(*) FROM history GROUP BY level")
    stats = c.fetchall()
    
    result = {
        "safe": 0,
        "first_level": 0,
        "second_level": 0
    }
    
    for level, count in stats:
        result[level] = count
    
    return result

@app.post("/api/login.php")
async def login(username: str, password: str):
    # 这里应该实现真实的用户认证逻辑
    if username == "admin" and password == "admin":
        return {"success": True}
    return {"success": False, "message": "用户名或密码错误"}

@app.post("/api/logout.php")
async def logout():
    return {"success": True}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 