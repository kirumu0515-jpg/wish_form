from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)
DATA_FILE = "data/wishes.json"

# JSONファイルがなければ作る
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    # フォームデータ取得
    name = request.form.get("name")
    wish = request.form.get("wish")
    color = request.form.get("color")
    hometown = request.form.get("hometown")

    # JSONに追加保存
    with open(DATA_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        data.append({
            "name": name,
            "wish": wish,
            "color": color,
            "hometown": hometown

              print(name, wish, color, hometown)

        })
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()

    return f"<h2>送信完了！{name}さんの灯籠を受け取りました🌕</h2>"

# oF 用 API：最新願い事を取得
@app.route("/api/wishes")
def api_wishes():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


  

    