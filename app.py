import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# 從 Render 環境變數抓 Key
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")

# --- 2. 路由處理 (Routing Logic) ---

# 首頁 '/' 的處理：顯示所有選項
@app.route('/')
def index():
    return render_template('index.html')

# 其他頁面路由 (它們必須在這裡!)
@app.route('/competition')
def competition():
    return render_template('competition.html')

@app.route('/activities')
def activities():
    return render_template('activities.html')

@app.route('/leadership')
def leadership():
    return render_template('leadership.html')

@app.route('/club')
def club():
    return render_template('club.html')

@app.route('/electives')
def electives():
    return render_template('electives.html')

@app.route('/ai', methods=['GET', 'POST'])
def ai():
    if request.method == 'GET':
        return render_template('ai.html')
    
    # POST 請求處理 AI
    data = request.get_json(silent=True) or {}
    user_input = data.get('question', '').strip()
    
    if not user_input:
        return jsonify({"answer": "歡迎……"})

    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    about_me = """
    你的任務是幫助使用者了解「我」。回答親切、像好友一樣
    - 特質：理性、穩定、有創新想法
    - 興趣：小說、音樂、繪畫、程式設計  
    - 個性：內向但能穩定上台報告，願意嘗試合適的比賽
    - 動機：貴校科系完全符合我的興趣與能力，期待在此深度學習
    """

    data = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": about_me},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        answer = result['choices'][0]['message']['content']
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": f"哎呀，AI 鬧脾氣了：{str(e)}"})


# 網頁 '/ask' 的處理：這是處理 POST 請求的核心
@app.route('/ask', methods=['GET', 'POST'])
def ask_question():
    q = ""
    a = ""

    if request.method == 'POST':
        # 這是處理 HTML Form 傳來的資料
        q = request.form.get('question', '').strip()
        
        if q:
            url = "https://api.mistral.ai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {MISTRAL_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "mistral-small-latest",
                "messages": [
                    {"role": "system", "content": "請把內容翻譯成中文或是英文。"},
                    {"role": "user", "content": q}
                ]
            }

            try:
                response = requests.post(url, headers=headers, json=data, timeout=10)
                response.raise_for_status()
                result = response.json()
                a = result['choices'][0]['message']['content']
            except Exception as e:
                a = f"抱歉，連線出了點問題：{str(e)}"
        else:
            a = "你什麼都沒說，我該怎麼讀懂你的心呢？"
        
    return render_template('ask.html', question=q, answer=a)

if __name__ == '__main__':
    app.run(debug=True)
