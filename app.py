from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

# ✅ CRITICAL FIX: tell Flask exactly where static & templates are
app = Flask(__name__, static_folder='static', template_folder='templates')

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT NOT NULL,
                  message TEXT NOT NULL,
                  created_at DATETIME NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# --- ROUTES ---
@app.route('/')
def home():
    # ✅ NOW uses your index.html + base.html + CSS
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute("INSERT INTO messages (name, email, message, created_at) VALUES (?, ?, ?, ?)",
                  (name, email, message, datetime.now()))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('contact.html')

@app.route('/admin/messages')
def admin_messages():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute("SELECT * FROM messages ORDER BY created_at DESC")
    messages = c.fetchall()
    conn.close()
    return render_template('admin_messages.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
