from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, HiddenField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from shop.models import User

class RegistrationForm(FlaskForm):
    username_new = StringField('Username', validators=[
        DataRequired(),
        Length(min=5, max=30),
    ])
    password_new = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=5, max=30),
    ])
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password_new', message='Passwords do not match. Try again.')
    ])
    submit = SubmitField('Register')

    def validate_username_new(self, username_new):
        user = User.query.filter_by(username=username_new.data).first()
        if user is not None:
            raise ValidationError('Username already exists, please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Username is required.")])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')