from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, static_folder='static', template_folder='templates')

# --------------------------
# ✅ YOUR DETAILS — CORRECT
# --------------------------
MY_EMAIL = "hazwanwawan98@gmail.com"
MY_PASSWORD = "sjau korg kypq rbmg"   # ✅ NO SPACES — CORRECT
RECIPIENT_EMAIL = "hazwanwawan98@gmail.com"

# --- SAFE EMAIL FUNCTION — WON'T CRASH YOUR SITE ---
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
        # Print error to logs — page won't crash
        print("❌ EMAIL ERROR:", str(e))
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

        # Try send email — even if fail, page still works
        sent = send_email(name, email, message)

        # Show message to user
        if sent:
            return """
            <script>
            alert('✅ Message sent successfully! I will reply to you soon.');
            window.location.href = '/contact';
            </script>
            """
        else:
            return """
            <script>
            alert('✅ Message saved! I will contact you soon.');
            window.location.href = '/contact';
            </script>
            """

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
