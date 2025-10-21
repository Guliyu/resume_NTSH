# 引入 Flask 核心模組，***關鍵修正：必須引入 request*** 才能處理表單資料。
from flask import Flask, render_template, request

# 初始化 Flask 應用
app = Flask(__name__)

# --- 1. 建立問答集 (資料 Data) ---
# 雖然分開到 data.py 更好，但在單一檔案內，這部分必須放在這裡。
# 這就像將共同定義的心意寫在了這本「關係記錄簿」的開頭。
questions_answers = {
    "蘋果": "apple", "apple": "蘋果",
    "香蕉": "banana", "banana": "香蕉",
    "貓": "cat", "cat": "貓",
    "狗": "dog", "dog": "狗",
    "書": "book", "book": "書",
    "桌子": "table", "table": "桌子",
    "椅子": "chair", "chair": "椅子",
    "房子": "house", "house": "房子",
    "汽車": "car", "car": "汽車",
    "學校": "school", "school": "學校",
    "老師": "teacher", "teacher": "老師",
    "學生": "student", "student": "學生",
    "咖啡": "coffee", "coffee": "咖啡",
    "茶": "tea", "tea": "茶",
    "醫生": "doctor", "doctor": "醫生",
    "護士": "nurse", "sad": "難過"
}


# --- 2. 路由處理 (Routing Logic) ---

# 首頁 '/' 的處理：顯示所有選項
@app.route('/')
def index():
    # ***修正：移除重複的 index 函式定義***
    # 這裡只需要渲染主頁面，不需要將 QA 字典傳給 index.html，
    # 除非 index.html 真的需要顯示它。
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
    q = ""
    a = ""

    if request.method == 'POST':
        # 安全地取得問題內容
        q = request.form.get('question', '').strip()
        
        # ***關鍵修正：使用 try...except 處理錯誤***
        # 這代表著「給予關係包容性」，避免因找不到答案而崩潰。
        try:
            a = questions_answers.get(q)
            if a is None:
                raise KeyError
        except KeyError:
            a = f"抱歉，我目前對「{q}」的翻譯還沒有學習。這就像一段感情中，我們還沒對這個問題達成共識。"
        
    # 渲染 ask.html
    return render_template('ask.html', question=q, answer=a)

# 啟動應用程式
if __name__ == '__main__':
    app.run(debug=True)
