from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('email', validators=[DataRequired(), Email(), Length(min=15, max=35)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Log In')
