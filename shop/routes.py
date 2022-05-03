from flask import render_template
from shop import app
import sys
from shop.models import User, Item, Category

@app.route("/")
def home():
    items = Item.query.all()
    categories = Category.query.all()
    return render_template('index.html', items=items, categories=categories)

@app.route("/product/<int:product_id>")
def product(product_id):
    item = Item.query.get_or_404(product_id)
    return render_template('product.html', item=item )

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/cart")
def cart():
    items = User.query.get_or_404(1).cart
    return render_template('cart.html', items=items)

@app.route("/checkout")
def checkout():
    items = User.query.get_or_404(1).cart
    return render_template('checkout.html', items=items)

@app.errorhandler(404)
def page_not_found(error):
    print(error, file=sys.stderr)
    return render_template('404.html')

