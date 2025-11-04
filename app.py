from flask import Flask, render_template, request
from pythonosc import udp_client
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("form.html")  # templates/form.html を使用

@app.route("/submit", methods=["POST"])
def submit():
    # フォームデータ取得
    name = request.form.get("name")
    wish = request.form.get("wish")
    color = request.form.get("color")
    hometown = request.form.get("hometown")

    # ログに出力
    print(name, wish, color, hometown)

    # OSC送信（Render内で完結する場合、サーバー自身のポートに送信）
    # Render サーバー内の OSC 受信プログラムに届くイメージ
    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
    client.send_message("/wish", [name, wish, color, hometown])

    return f"<h2>送信完了！{name}さんの灯籠を受け取りました🌕</h2>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
