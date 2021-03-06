from flask import Flask, render_template, request, flash, g
import sqlite3
import os
from fdatabase import FDataBase
# конфигурация
DATABASE = '/tmp/chat.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
USERNAME = 'admin'
PASSWORD = '123'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'chat.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_chat.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route('/', methods=['POST', 'GET'])
def index():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if request.form['name'] and request.form['message']:
            res = dbase.addMessage(request.form['name'], request.form['message'])
            if not res:
                flash('Ошибка отправки сообщения', category = 'error')
            else:
                flash('Сообщение отправлено', category='success')
    return render_template('index.html', title='Simple chat', messages=dbase.getHistoryMessages())

if __name__ == '__main__':
    app.run(debug=True)
