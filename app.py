from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Environment variables — safe for Render
MY_EMAIL = os.getenv("MY_EMAIL", "hazwanwawan98@gmail.com")
MY_PASSWORD = os.getenv("MY_PASSWORD", "")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "hazwanwawan98@gmail.com")

def send_email(name, email, message):
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
        server.starttls()
        server.login(MY_EMAIL, MY_PASSWORD.strip())
        server.sendmail(MY_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("❌ Email error:", str(e))
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
        name = request.form.get('name', 'No Name')
        email = request.form.get('email', 'No Email')
        message = request.form.get('message', 'No Message')
        sent = send_email(name, email, message)
        if sent:
            return "<script>alert('✅ Message sent!');history.back();</script>"
        else:
            return "<script>alert('⚠️ Could not send now.');history.back();</script>"
    return render_template('contact.html')

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
