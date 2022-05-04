from flask import request, render_template, redirect, url_for, flash, session
from shop import app, db
from shop.models import User, Item, Category
from shop.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user
from sqlalchemy import asc, desc

@app.route("/", methods=['GET', 'POST'])
def home():
    category_id = 0
    sort = 'price_low'

    if request.method == 'POST':
        form_name = request.form['form_name']
        if form_name == 'sort_items':
            sort = request.form['sort']
            category_id = int(request.form['category_id'])
        elif form_name == 'filters':
            category_id = int(request.form['filter_items'])
            sort = request.form['sort']
        elif form_name == 'add_to_cart':
            category_id = int(request.form['category_id'])
            sort = request.form['sort']

            if current_user.is_authenticated:
                item_id = int(request.form['add_to_cart'])
                item = Item.query.filter_by(id=item_id).first()
                if item:
                    if item in current_user.cart:
                        flash(f'{item.name} is already in your cart.')
                    else:
                        current_user.cart.append(item)
                        db.session.commit()
                        flash(f'{item.name} has been added to your cart.')
                else:
                    flash('Could not find item.')
            else:
                flash('You must be logged in to add an item to your cart.')
    
    order_by = None
    if sort == 'price_low':
        order_by = asc(Item.price)
    elif sort == 'price_high':
        order_by = desc(Item.price)
    else:
        order_by = asc(Item.carbon)
    
    categories = Category.query.all()
    items = []
    if category_id == 0:
        items = Item.query.order_by(order_by)
    else:
        items = Item.query.filter_by(category_id=category_id).order_by(order_by)

    return render_template('index.html', items=items, categories=categories, category_id=category_id, sort=sort)

@app.route("/product/<int:product_id>")
def product(product_id):
    item = Item.query.get_or_404(product_id)
    return render_template('product.html', item=item )

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Your are already logged in.')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        flash('You have been successfully logged in.')
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username_new.data, password=form.password_new.data)
        db.session.add(user)
        db.session.commit()
        flash('You have been successfully registered.')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    was_logged_in = current_user.is_authenticated
    logout_user()
    if was_logged_in:
        flash('You have been successfully logged out.')
    else:
        flash('You are already logged out.')
    return redirect(url_for('home'))

@app.route("/cart", methods=['GET', 'POST'])
def cart():
    if not current_user.is_authenticated:
        flash('You must be logged in to access your cart.')
        return redirect(url_for('home'))
    items = current_user.cart

    if request.method == 'POST':
        item_id = int(request.form['remove_item'])
        item = Item.query.filter_by(id=item_id).first()
        if item:
            current_user.cart.remove(item)
            db.session.commit()
            flash(f'{item.name} has been removed from your cart.')
        else:
            flash('Could not find item.')

    return render_template('cart.html', items=items)

@app.route("/checkout")
def checkout():
    if not current_user.is_authenticated:
        flash('You must be logged in to checkout.')
        return redirect(url_for('home'))
    if len(current_user.cart) < 1:
        flash("You dont have anything in your cart to checkout.")
        return redirect(url_for('home'))
    items = current_user.cart
    return render_template('checkout.html', items=items)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

