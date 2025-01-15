from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('bingo.db')
    c = conn.cursor()
    # 刪除舊表（如果存在）
    c.execute('DROP TABLE IF EXISTS grid_counts')
    # 重新創建表，包含名稱列
    c.execute('''CREATE TABLE grid_counts (
        cell INTEGER PRIMARY KEY, name TEXT, count INTEGER
    )''')

    # 初始化數據
    names = [
        "飯戲攻心2", "淺淺歲月", "12怪盜", "聲影路", "裡應外合", "紮職3", "臨時劫案",
        "維和防暴隊", "Bonus 去年戲院遇過明星", "久別重逢", "十方之地", "錄影歹", "重生", "反貪風暴之加密危機",
        "超意神探", "危機航線", "盜月者", "冬未來", "紅豆", "出租家人", "從今以後",
        "傳說", "得寵先生", "手機見鬼", "破·地獄", "Bonus 去年試過全院少於三人睇戲", "海關戰線", "看我今天怎麼說",
        "虎毒不", "我談的那場戀愛", "邪Mall", "只是影畫", "談判專家", "山莊日記", "焚城",
        "愛情城事", "查無此人", "望月", "香港四徑大步走", "誤判", "紅毯先生", "敗走麥城",
        "爸爸", "把幸福拉近一點", "寄了一整個春天", "公開試當真", "九龍城寨之圍城", "武替道", "Bonus Follow 咗 Wave."
    ]
    for i, name in enumerate(names, start=1):
        c.execute('INSERT INTO grid_counts (cell, name, count) VALUES (?, ?, ?)', (i, name, 0))
    conn.commit()
    conn.close()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    user = data.get('user', 'anonymous')
    answers = data.get('answers', '')
    conn = sqlite3.connect('bingo.db')
    c = conn.cursor()
    # 保存用戶答案
    c.execute('INSERT INTO answers (user, answers) VALUES (?, ?)', (user, answers))
    # 更新格子選擇次數
    for cell in map(int, answers.split(',')):
        c.execute('UPDATE grid_counts SET count = count + 1 WHERE cell = ?', (cell,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/grid-data', methods=['GET'])
def grid_data():
    conn = sqlite3.connect('bingo.db')
    c = conn.cursor()
    c.execute('SELECT cell, count FROM grid_counts')
    grid_counts = {row[0]: row[1] for row in c.fetchall()}
    conn.close()
    return jsonify(grid_counts)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
