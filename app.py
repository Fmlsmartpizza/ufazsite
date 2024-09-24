from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)


db_path = 'users.db'


def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def add_user(username, password):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # SQL-запрос для вставки нового пользователя
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    
    # Сохранение изменений в базе данных
    conn.commit()
    conn.close()


def user_exists(username):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

@app.route('/')
def home():
    return render_template('home.html', error=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('register.html', error="Both fields are required.")

        
        if user_exists(username):
            return render_template('register.html', error="A user with the same name already exists!")

        
        add_user(username, password)
        return render_template('register.html', success="Registered successfully!")
    
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return "Logged in successfully!"  
        else:
            return render_template('login.html', error="Invalid username or password.")

    return render_template('login.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
