from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, make_response
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

# Security settings
app.secret_key = os.getenv("SECRET_KEY", "aimecha-dev-key-only")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "aimecha123")

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=7)
db = SQLAlchemy(app)

# Message model
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
# ✅ GOOGLE VERIFICATION
# --------------------------
@app.route('/google2cd12ac9bec35551.html')
def google_verify():
    return send_from_directory('.', 'google2cd12ac9bec35551.html')

# --------------------------
# ✅ SEO: ROBOTS.TXT & VALID SITEMAP
# --------------------------
@app.route('/robots.txt')
def robots():
    txt = """User-agent: *
Allow: /
Sitemap: https://aimecha-initiatives.onrender.com/sitemap.xml
"""
    response = make_response(txt)
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    return response

@app.route('/sitemap.xml')
def sitemap():
    base_url = "https://aimecha-initiatives.onrender.com"
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{base_url}/</loc>
    <lastmod>2026-06-17</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{base_url}/about</loc>
    <lastmod>2026-06-17</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>{base_url}/services</loc>
    <lastmod>2026-06-17</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>{base_url}/contact</loc>
    <lastmod>2026-06-17</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>"""

    response = make_response(xml)
    response.headers["Content-Type"] = "application/xml; charset=utf-8"
    response.headers["Cache-Control"] = "public, max-age=86400"
    return response

# --------------------------
# MAIN ROUTES
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

        new_msg = Message(name=name, email=email, message=message)
        db.session.add(new_msg)
        db.session.commit()

        flash('✅ Message saved successfully!')
        return redirect(url_for('contact'))

    return render_template('contact.html')

# --------------------------
# ADMIN ROUTES
# --------------------------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
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
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

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
