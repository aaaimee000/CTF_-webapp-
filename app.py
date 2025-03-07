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
            username TEXT UNIQUE,
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
    
    # New tables for video/key with UNIQUE constraints to avoid duplicates
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY,
            encrypted_video BLOB
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keys_table (
            id INTEGER PRIMARY KEY,
            decryption_key TEXT UNIQUE
        )
    ''')
    
    # Insert encrypted video and key (do this once)
    # Read the encrypted video file as binary
    with open('secret_video.enc', 'rb') as f:
        encrypted_data = f.read()

    # Use a fixed id for videos to avoid duplicate entries
    cursor.execute("INSERT OR IGNORE INTO videos (id, encrypted_video) VALUES (1, ?)", 
                   (encrypted_data,))
    
    # The UNIQUE constraint on decryption_key will ensure no duplicate keys are inserted
    cursor.execute("INSERT OR IGNORE INTO keys_table (decryption_key) VALUES (?)",
                   ('OMNI_AI_VIDEO_KEY_619',))  # Key to extract via SQLi
    
    # OLD FLAG __ CAN BE DELETED __ Insert admin user with flag
    cursor.execute("INSERT OR IGNORE INTO users (username, password, flag) VALUES (?, ?, ?)",
                   ('admin', 'password123', 'FLAG_SQLI_123--TESTEST'))
    
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_video')
def get_video():
    video_id = request.args.get('id', 1)  # Default to ID 1
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT encrypted_video FROM videos WHERE id = ?", (video_id,))
    video_blob = cursor.fetchone()[0]
    
    conn.close()
    
    # Serve the encrypted video
    response = make_response(video_blob)
    response.headers.set('Content-Type', 'video/mp4')
    response.headers.set('Content-Disposition', 'attachment', filename='secret_video.enc')
    return response

# SQL Injection Challenge
@app.route('/sqli-login', methods=['GET', 'POST'])
def sqli_login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        conn = get_db()
        cursor = conn.cursor()
        
        # Vulnerable query without the JOIN permissions
        query = f"""
        SELECT * FROM users 
        WHERE username = '{username}' 
        AND password = '{password}'
        """
        
        try:
            cursor.execute(query)
            user = cursor.fetchone()
            if user:
                # Using user[0] to display the flag means our SQL injection payload must
                # return the decryption key as the first column.
                message = f"Flag: {user[0]} | Access /get_video?id=1"
            else:
                message = "ACCESS DENIED: Insufficient clearance."
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
        resp.set_cookie('flag', 'GOTCHU! Wrong way - look for the key somewhere else human.')
        return resp

if __name__ == '__main__':
    app.run(debug=True)
