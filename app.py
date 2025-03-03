from flask import Flask, request, render_template, redirect, make_response
import sqlite3

app = Flask(__name__)

# Database configuration
DATABASE = 'ctf.db'

def get_db():
    return sqlite3.connect(DATABASE)

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            flag TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY,
            content TEXT
        )
    ''')
    # Insert admin user with flag
    cursor.execute("INSERT OR IGNORE INTO users (username, password, flag) VALUES (?, ?, ?)",
                   ('admin', 'password123', 'FLAG_SQLI_123'))
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

# SQL Injection Challenge
@app.route('/sqli-login', methods=['GET', 'POST'])
def sqli_login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        conn = get_db()
        cursor = conn.cursor()
        # Vulnerable SQL query
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        try:
            cursor.execute(query)
            user = cursor.fetchone()
            if user:
                message = f"Flag: {user[3]}"  # Display flag from the database
            else:
                message = "Login failed!"
        except sqlite3.Error as e:
            message = "Error: " + str(e)
        conn.close()
    return render_template('sqli_login.html', message=message)

# XSS Challenge
@app.route('/xss-comment', methods=['GET', 'POST'])
def xss_comment():
    if request.method == 'POST':
        comment = request.form.get('comment', '')
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO comments (content) VALUES (?)", (comment,))
        conn.commit()
        conn.close()
        return redirect('/xss-comment')
    else:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM comments")
        comments = [row[0] for row in cursor.fetchall()]
        conn.close()
        resp = make_response(render_template('xss_comment.html', comments=comments))
        resp.set_cookie('flag', 'FLAG_XSS_COOKIE_456')
        return resp

if __name__ == '__main__':
    app.run(debug=True)