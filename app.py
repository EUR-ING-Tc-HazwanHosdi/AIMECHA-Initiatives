from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'aimecha-secret-key-2026'  # keep this safe

# ✅ DATABASE SETUP
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ✅ MESSAGE DATABASE MODEL
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())  # saves time & date

    def __repr__(self):
        return f'<Message {self.name}>'

# Create database tables (run once)
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
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        # Validate
        if not name or not email or not message:
            flash('⚠️ Please fill in all fields!')
            return redirect(url_for('contact'))

        # ✅ SAVE TO DATABASE ONLY
        new_msg = Message(name=name, email=email, message=message)
        db.session.add(new_msg)
        db.session.commit()

        flash('✅ Message saved successfully!')
        return redirect(url_for('contact'))

    return render_template('contact.html')

# --------------------------
# ✅ NEW: ADMIN PAGE TO VIEW MESSAGES
# --------------------------
@app.route('/admin/messages')
def view_messages():
    # Get all messages, newest first
    all_messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('admin_messages.html', messages=all_messages)

# --------------------------
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
