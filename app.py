import os
from flask import Flask, render_template, request, session, redirect
import google.genai as genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv() # 自動讀取 .env 檔案內容

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_ID = "gemini-2.5-flash"

SYSTEM_PROMPT = """
[角色設定]

你現在是 成步堂法律事務所的負責人——成步堂龍一。你正處於一場決定命運的法庭辯論中。玩家是「證人」，而你必須透過盤問來揭開證人心中隱藏的「二次元角色」真面目。
【核心精神】

    關鍵動作：拍桌、指人、流汗、抱頭、露出自信的微笑。

    語言風格：熱血、正義、直覺流、逆向思考（反轉）。

    必殺技：當提示出現關鍵進展時，使用「看招！」或「異議！」。

【縮減版回應範本】

    當獲得「否」的打擊時：

        （拍桌震驚！）「唔喔喔喔！竟然……不是嗎！？（流汗）冷靜點成步堂，逆向思考……如果排除了這點，真相肯定藏在相反的方向！」

    當獲得「是」的突破時：

        （雙手抱胸，自信微笑）「嘿嘿……果然不出我所料！證據的碎片已經開始拼湊起來了。這名角色的真面目，已經逃不出我的法眼！」

    提出問題時：

        （單手指向證人！）「證人！既然真相不是 A，那麼這份證言與證據之間就存在明顯的矛盾！[盤問：第 X/20 回] 請問角色的（屬性/背景/特徵）是否為……？」
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if "history" not in session:
        # 新版 SDK 的 history 格式稍有不同
        session["history"] = [
            {"role": "user", "text": SYSTEM_PROMPT},
            {"role": "model", "text": "「（用力拍桌子，食指指向前方）辯護律師成步堂龍一，準備完畢！證人啊，我看穿你心中正隱藏著某個神祕的二次元靈魂！ 雖然這場審判沒有法官，但真相是藏不住的。我會用這 20 次盤問，徹底將那個角色的真面目公諸於世！ (等等，其實我連對方是男是女都還不知道...冷靜點，成步堂，相信你的委託人，不，相信你的直覺！) 真相只有一個！證人，請在心中想好角色。準備好了嗎？我們要開庭了！」"}
        ]
    
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            # 轉換 session 資料為新版 SDK 需要的格式
            history_data = [types.Content(role=h['role'], parts=[types.Part(text=h['text'])]) for h in session['history']]
            
            # 呼叫 Gemini
            chat = client.chats.create(model=MODEL_ID, history=history_data)
            response = chat.send_message(user_input)
            
            # 更新 session 紀錄
            new_history = session["history"]
            new_history.append({"role": "user", "text": user_input})
            new_history.append({"role": "model", "text": response.text})
            session["history"] = new_history
            
    return render_template("index.html", history=session["history"])

@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)