from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "data/wishes.json"

# -----------------------------
# フォームページ
# -----------------------------
@app.route("/")
def index():
    return render_template("form.html")

# -----------------------------
# フォーム送信
# -----------------------------
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "")
    wish = request.form.get("wish", "")
    color = request.form.get("color", "")
    hometown = request.form.get("hometown", "")

    # 保存用ディレクトリ作成
    if not os.path.exists("data"):
        os.makedirs("data", exist_ok=True)

    # JSON ファイルが存在しなければ作成
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    # 既存データ読み込み
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            wishes = json.load(f)
        except json.JSONDecodeError:
            wishes = []

    # 新しいデータを追加
    wishes.append({
        "name": name,
        "wish": wish,
        "color": color,
        "hometown": hometown
    })

    # ファイルに保存
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(wishes, f, ensure_ascii=False, indent=2)

    return f"<h2>送信完了！{name}さんの灯籠を受け取りました🌕</h2>"

# -----------------------------
# API: JSON データを返す
# -----------------------------
@app.route("/api/wishes")
def get_wishes():
    # ファイルがなければ空配列を返す
    if not os.path.exists(DATA_FILE):
        os.makedirs("data", exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            wishes = json.load(f)
        except json.JSONDecodeError:
            wishes = []

    return jsonify(wishes)  # ← ここがポイント

# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
