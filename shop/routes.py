from flask import request, render_template, redirect, url_for, flash
from shop import app, db
from shop.models import User, Item, Category, Review
from shop.forms import LoginForm, RegistrationForm, ReviewForm, CheckoutForm
from flask_login import login_user, logout_user, current_user
from sqlalchemy import asc, desc

@app.route("/", methods=['GET', 'POST'])
def home():
    category_id = 0
    sort = 'price_high'

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
                    elif item in current_user.inventory:
                        flash(f'You already own {item.name}.')
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

@app.route("/product/<int:product_id>", methods=['GET', 'POST'])
def product(product_id):
    item = Item.query.get_or_404(product_id)
    form = ReviewForm()

    if request.method == 'POST':            
        form_name = request.form['form_name']
        if form_name == 'add_to_cart':
            if current_user.is_authenticated:
                item_id = int(request.form['add_to_cart'])
                item = Item.query.filter_by(id=item_id).first()
                if item:
                    if item in current_user.cart:
                        flash(f'{item.name} is already in your cart.')
                    elif item in current_user.inventory:
                        flash(f'You already own {item.name}.')
                    else:
                        current_user.cart.append(item)
                        db.session.commit()
                        flash(f'{item.name} has been added to your cart.')
                else:
                    flash('Could not find item.')
            else:
                flash('You must be logged in to add an item to your cart.')
        else:
            if not current_user.is_authenticated:
                flash('You must be logged in to review an item.')
            else:
                review = Review(rating=form.rating.data, title=form.title.data , text=form.text.data, item_id=item.id)
                review.user = current_user
                item.reviews.append(review)
                db.session.commit()
                flash(f'Your review has been added to {item.name}')
    return render_template('product.html', item=item, form=form )

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Your are already logged in.')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            login_user(user)
            flash('You have been successfully logged in.')
            return redirect(url_for('home'))
        else:
            flash('Invalid password or username.')
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
        if item and item in current_user.cart:
            current_user.cart.remove(item)
            db.session.commit()
            flash(f'{item.name} has been removed from your cart.')
        else:
            flash('Could not find item.')

    total_price = 0
    for item in items:
        total_price += item.price
    return render_template('cart.html', items=items, total_price=total_price)

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        flash('You must be logged in to view your profile.')
        return redirect(url_for('home'))

    if request.method == 'POST':            
        form_name = request.form['form_name']
        if form_name == 'delete_review':
            review_id = request.form['delete_review']
            Review.query.filter_by(id=review_id).delete()
            db.session.commit()
            flash('Review has been deleted.')
        elif form_name == 'sell_item':
            item_id = request.form['sell_item']
            item = Item.query.filter_by(id=item_id).first()
            if item and item in current_user.inventory:
                current_user.inventory.remove(item)
                db.session.commit()
                flash(f'You have sold {item.name} for £{item.price}. The money has been transferred to the bank account that bought it.')
    return render_template('profile.html')

@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    if not current_user.is_authenticated:
        flash('You must be logged in to checkout.')
        return redirect(url_for('home'))
    if len(current_user.cart) < 1:
        flash("You dont have anything in your cart to checkout.")
        return redirect(url_for('home'))

    form = CheckoutForm()
    items = current_user.cart
    if form.validate_on_submit():
        current_user.inventory.extend(current_user.cart)
        current_user.cart = []
        db.session.commit()
        flash("Checkout successful.")
        return redirect(url_for('profile'))
    
    total_price = 0
    for item in items:
        total_price += item.price
    return render_template('checkout.html', items=items, form=form, total_price=total_price)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

