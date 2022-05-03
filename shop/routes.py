from urllib import request
from flask import request, render_template, redirect, url_for, flash
from shop import app
import sys
from shop.models import User, Item, Category
from shop.forms import LoginForm, RegistrationForm
from shop import db
from flask_login import login_user, logout_user, current_user

@app.route("/", methods=['GET', 'POST'])
def home():
    items = Item.query.all()
    categories = Category.query.all()
    # if request.method == 'POST':
        # if current_user.is_authenticated:
        #     item_id = int(request.form['add_to_cart'])
        #     item = Item.query.filter_by(id=item_id).first()
        #     if item:
        #         current_user.cart.append(item)
        #         db.session.commit()
        #         # flash('item added')
    if request.method == 'POST':
        filter_id = int(request.form['filter_items'])
        if filter_id != 0:
            items = Item.query.filter_by(category_id=filter_id)

    return render_template('index.html', items=items, categories=categories)

@app.route("/product/<int:product_id>")
def product(product_id):
    item = Item.query.get_or_404(product_id)
    return render_template('product.html', item=item )

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        # flash
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    # flash
    return redirect(url_for('home'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username_new.data, password=form.password_new.data)
        db.session.add(user)
        db.session.commit()
        # flash('You have been successfully registered!!', )
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route("/cart")
def cart():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    items = current_user.cart
    return render_template('cart.html', items=items)

@app.route("/checkout")
def checkout():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    items = current_user.cart
    return render_template('checkout.html', items=items)

@app.errorhandler(404)
def page_not_found(error):
    print(error, file=sys.stderr)
    return render_template('404.html')

