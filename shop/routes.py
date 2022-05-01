from flask import render_template
from shop import app
import sys

@app.route("/")
def home_page():
    return render_template('index.html')

@app.route("/login")
def login_page():
    return render_template('login.html')

@app.route("/register")
def register_page():
    return render_template('register.html')

@app.route("/cart")
def cart_page():
    return render_template('cart.html')

@app.route("/checkout")
def checkout_page():
    return render_template('checkout.html')

@app.errorhandler(404)
def page_not_found(error):
    print(error, file=sys.stderr)
    return render_template('404.html')

