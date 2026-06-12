from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, static_folder='static', template_folder='templates')

# --------------------------
# ✅ CHANGE THESE 3 THINGS
# --------------------------
MY_EMAIL = "hazwanwawan98@gmail.com"       # ← YOUR EMAIL
MY_PASSWORD = "tnqdxlckmddntpdo"       # ← YOUR GMAIL APP PASSWORD (explained below)
RECIPIENT_EMAIL = "hazwanwawan98@gmail.com" # ← WHERE TO RECEIVE MESSAGES

# --- SEND EMAIL FUNCTION ---
def send_email(name, email, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = MY_EMAIL
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = "📩 NEW MESSAGE FROM AIMECHA WEBSITE"

        body = f"""
NEW CONTACT FORM SUBMISSION:

Name: {name}
Email / WhatsApp: {email}

Message:
{message}

---
Received from: https://aimecha-initiatives.onrender.com
        """
        msg.attach(MIMEText(body, "plain"))

        # Send via Gmail
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(MY_EMAIL, MY_PASSWORD)
        server.sendmail(MY_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Error:", e)
        return False

# --- ROUTES ---
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
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Send to your email
        send_email(name, email, message)

        # Show success message
        return """
        <script>
        alert('✅ Message sent successfully! I will reply to you soon.');
        window.location.href = '/contact';
        </script>
        """
    return render_template('contact.html')

# ❌ REMOVED /admin/messages route — NO MORE ERRORS

if __name__ == '__main__':
    app.run(debug=True)
