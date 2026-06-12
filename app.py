from flask import Flask, render_template

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return "<h1>Welcome to My Website Service</h1><p>I build professional websites for small businesses — fast, free setup, affordable price.</p>"

# About page
@app.route('/about')
def about():
    return "<h1>About Me</h1><p>I create websites using Python — secure, easy to update, mobile-friendly.</p>"

# Services page
@app.route('/services')
def services():
    return "<h1>My Services</h1><ul><li>Business Website — RM800</li><li>Landing Page — RM500</li><li>Website Maintenance — RM150/month</li></ul>"

if __name__ == '__main__':
    app.run(debug=True)