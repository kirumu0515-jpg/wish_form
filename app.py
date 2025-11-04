from flask import Flask, request, render_template
from pythonosc import udp_client

app = Flask(__name__)

client = udp_client.SimpleUDPClient("127.0.0.1", 12345)

# フォームページを返す
@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        "name": request.form['name'],
        "wish": request.form['wish'],
        "color": request.form['color'],
        "hometown": request.form['hometown']
    }
    print("受け取ったデータ:", data)
    
    client.send_message("/wish", [data["name"], data["wish"], data["color"], data["hometown"]])
    
    return "データを受け取りました！"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
