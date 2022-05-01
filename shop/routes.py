from turtle import pos
from flask import render_template, url_for
from shop import app
import sys

posts = [
        {
            'name': 'Sandbox',
            'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation',
            'picture': 'https://venturebeat.com/wp-content/uploads/2021/03/article23-1.jpg?w=1200&strip=all',
            'price': 20,
            'carbon': 30
        },
        {
            'name': 'Decentraland',
            'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation',
            'picture': 'https://venturebeat.com/wp-content/uploads/2022/03/GettyImages-937126612.jpg?fit=1732%2C990&strip=all',
            'price': 15,
            'carbon': 80
        },
        {
            'name': 'Deltaverse',
            'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation',
            'picture': 'https://robbreport.com/wp-content/uploads/2022/02/RR_Metaverse_02.jpg',
            'price': 120,
            'carbon': 5
        },
        {
            'name': 'MV DOA',
            'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation',
            'picture': 'http://wearemtm.com/wp-content/uploads/2022/04/metaverse-virtual-world-1.png',
            'price': 90,
            'carbon': 45
        },
    ]

@app.route("/")
def home():
    return render_template('index.html', posts=posts)

@app.route("/product")
def product():
    return render_template('product.html', post=posts[0])

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/cart")
def cart():
    return render_template('cart.html', posts=[posts[0], posts[1], posts[2]])

@app.route("/checkout")
def checkout():
    return render_template('checkout.html', posts=[posts[0], posts[1], posts[2]])

@app.errorhandler(404)
def page_not_found(error):
    print(error, file=sys.stderr)
    return render_template('404.html')

