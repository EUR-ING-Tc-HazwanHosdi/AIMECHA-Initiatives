from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# ✅ Environment Variables — SET THESE IN RENDER
MY_EMAIL = os.getenv("MY_EMAIL", "").strip()
MY_PASSWORD = os.getenv("MY_PASSWORD", "").strip()
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "").strip()

def send_email(name, email, message):
    if not MY_EMAIL or not MY_PASSWORD or not RECIPIENT_EMAIL:
        print("❌ Missing credentials!")
        return False
    try:
        msg = MIMEMultipart()
        msg["From"] = MY_EMAIL
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = "📩 New Message — AIMeCHA Website"
        body = f"""
Name: {name}
Email: {email}
Message:
{message}
---
From: AIMeCHA Website
        """
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(MY_EMAIL, MY_PASSWORD)
        server.sendmail(MY_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("❌ Error:", str(e))
        return False

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
            return "<script>alert('⚠️ Please fill all fields!');history.back();</script>"
        sent = send_email(name, email, message)
        if sent:
            return "<script>alert('✅ Message sent successfully!');history.back();</script>"
        else:
            return "<script>alert('❌ Failed to send. Check settings!');history.back();</script>"
    return render_template('contact.html')

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
