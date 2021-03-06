from random import choices
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from shop.models import User

class RegistrationForm(FlaskForm):
    username_new = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(min=5, max=30, message="Username must be between 5 and 30 characters long."),
    ])
    password_new = PasswordField('Password', validators=[
        DataRequired("Password is required."),
        Length(min=5, max=30, message="Password must be between 5 and 30 characters long."),
    ])
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired("Confirm Password is required."),
        EqualTo('password_new', message='Passwords do not match. Try again.')
    ])
    submit = SubmitField('Register')

    def validate_username_new(self, username_new):
        user = User.query.filter_by(username=username_new.data).first()
        if user is not None:
            raise ValidationError('Username already exists, please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Username is required.")])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required.")])
    submit = SubmitField('Log In')

class ReviewForm(FlaskForm):
    rating = RadioField('Rating', validators=[DataRequired(message="Rating is required.")], choices=['1', '2', '3', '4', '5'])
    title = StringField('Title', validators=[DataRequired(message="Title is required."), Length(min=3, max=120, message="Title must be between 3 and 120 characters long.")])
    text = TextAreaField('Review', validators=[Length(max=240, message="Review must be 240 or less characters long.")])
    submit = SubmitField('Review Product')

class CheckoutForm(FlaskForm):
    name = StringField("Card Holder's Name", validators=[DataRequired(message="Card Holder's name is required.")])
    card_no = IntegerField('Card Number', validators=[DataRequired(message="Card Number is required.")])
    submit = SubmitField('Checkout')

    def validate_card_no(self, card_no):
        if len(str(card_no.data)) != 16:
            raise ValidationError(f'Card Number must be 16 digits long.')
