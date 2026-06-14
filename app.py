from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import timedelta

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'aimecha-secret-key-2026'  # Keep this secret!

# ✅ DATABASE SETUP
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=7)  # Stay logged in 7 days
db = SQLAlchemy(app)

# ✅ SET YOUR PASSWORD HERE (change it if you want)
ADMIN_PASSWORD = 'aimecha123'  # ← YOUR PASSWORD

# ✅ MESSAGE DATABASE MODEL
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<Message {self.name}>'

with app.app_context():
    db.create_all()

# --------------------------
# ROUTES
# --------------------------
@app.route('/')
def home():
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
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            flash('⚠️ Please fill in all fields!')
            return redirect(url_for('contact'))

        # ✅ SAVE ONLY TO DATABASE
        new_msg = Message(name=name, email=email, message=message)
        db.session.add(new_msg)
        db.session.commit()

        flash('✅ Message saved successfully!')
        return redirect(url_for('contact'))

    return render_template('contact.html')

# --------------------------
# ✅ ADMIN LOGIN & PROTECTED PAGE
# --------------------------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # If already logged in → go straight to messages
    if session.get('admin_logged_in'):
        return redirect(url_for('view_messages'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_PASSWORD:
            session.permanent = True
            session['admin_logged_in'] = True
            flash('✅ Login successful!')
            return redirect(url_for('view_messages'))
        else:
            flash('❌ Wrong password — try again.')

    return render_template('admin_login.html')

@app.route('/admin/messages')
def view_messages():
    # Only accessible if logged in
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    # Show all messages (newest first)
    all_messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('admin_messages.html', messages=all_messages)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('🔓 Logged out successfully.')
    return redirect(url_for('admin_login'))

# --------------------------
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
