from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

# JSON ファイルのパス
DATA_FILE = "data/wishes.json"

# data フォルダがなければ作成し、JSON を初期化
if not os.path.exists(DATA_FILE):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    wish = request.form.get("wish")
    color = request.form.get("color")
    hometown = request.form.get("hometown")

    # JSON に追加
    with open(DATA_FILE, "r+", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []  # 空ファイルや壊れた JSON の場合
        data.append({
            "name": name,
            "wish": wish,
            "color": color,
            "hometown": hometown
        })
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()

    return f"<h2>送信完了！{name}さんの灯籠を受け取りました🌕</h2>"

# oF 用 API: JSON を返す
@app.route("/api/wishes")
def api_wishes():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
