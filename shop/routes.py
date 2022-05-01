from flask import render_template, url_for
from shop import app
import sys

@app.route("/")
def home():
    posts = [
        {
            'name': 'Sandbox',
            'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation',
            'picture': 'https://venturebeat.com/wp-content/uploads/2021/03/article23-1.jpg?w=1200&strip=all',
            'price': 20,
            'carbon': 30
        },
        {
            'name': 'Sandbox',
            'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation',
            'picture': 'https://venturebeat.com/wp-content/uploads/2021/03/article23-1.jpg?w=1200&strip=all',
            'price': 20,
            'carbon': 30
        },
        {
            'name': 'Sandbox',
            'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation',
            'picture': 'https://venturebeat.com/wp-content/uploads/2021/03/article23-1.jpg?w=1200&strip=all',
            'price': 20,
            'carbon': 30
        },
        {
            'name': 'Sandbox',
            'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation',
            'picture': 'https://venturebeat.com/wp-content/uploads/2021/03/article23-1.jpg?w=1200&strip=all',
            'price': 20,
            'carbon': 30
        },
    ]
    return render_template('index.html', posts=posts)

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/cart")
def cart():
    return render_template('cart.html')

@app.route("/checkout")
def checkout():
    return render_template('checkout.html')

@app.errorhandler(404)
def page_not_found(error):
    print(error, file=sys.stderr)
    return render_template('404.html')

