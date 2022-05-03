from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length, Regexp
from shop.models import User

class RegistrationForm(FlaskForm):
    username_new = StringField('Username', validators=[
        DataRequired(),
        Length(min=5, max=30),
    ])
    password_new = StringField('Password', validators=[
        DataRequired(),
        Length(min=5, max=30),
    ])
    password_confirm = StringField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password_new', message='Passwords do not match. Try again.')
    ])
    submit = SubmitField('Register')

    def validate_username_new(self, username_new):
        user = User.query.filter_by(username=username_new.data).first()
        if user is not None:
            raise ValidationError('Username already exists, please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')