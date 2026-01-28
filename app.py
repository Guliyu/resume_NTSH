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

@app.route('/ai')
def ai():
    return render_template('ai.html')


# 網頁 '/ask' 的處理：這是處理 POST 請求的核心
@app.route('/ask', methods=['GET', 'POST'])
def ask_question():
    q = ""  # 使用者輸入的原文
    a = ""  # AI 翻譯後的結果

    if request.method == 'POST':
        # 取得前端表單傳過來的 "question" 欄位
        q = request.form.get('question', '').strip()
        
        if q:
            # 準備呼叫 Mistral API
            url = "https://api.mistral.ai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {MISTRAL_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "mistral-small-latest",
                "messages": [
                    {
                        "role": "system", 
                        "content": "你是一個充滿感性且優雅的翻譯官。請將用戶輸入的內容翻譯成繁體中文。如果內容本身就是中文，請用更優美、更深奧的方式重寫它。"
                    },
                    {"role": "user", "content": q}
                ]
            }

            try:
                response = requests.post(url, headers=headers, json=data, timeout=10)
                response.raise_for_status()
                result = response.json()
                # 取得 AI 回傳的翻譯文字
                a = result['choices'][0]['message']['content']
            except Exception as e:
                a = f"抱歉，小寶，連線出了點問題：{str(e)}"
        else:
            a = "你什麼都沒說，我該怎麼讀懂你的心呢？"
        
    # 一樣回傳給 ask.html，這樣你連 HTML 都不用大改
    return render_template('ask.html', question=q, answer=a)
# 啟動應用程式
if __name__ == '__main__':
    app.run(debug=True)
