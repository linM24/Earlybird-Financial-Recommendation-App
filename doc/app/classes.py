from flask import Flask
from flask_login import UserMixin
from flask_wtf import FlaskForm

from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import  DateField, IntegerField, PasswordField, SelectField, StringField, SubmitField, FloatField
from wtforms.validators import DataRequired

from app import db, login_manager

class Project(db.Model):
    """
    Porject Class
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    Net_Wealth = db.Column(db.Float, nullable=False)
    Annual_Income = db.Column(db.Float,  nullable=False)
    Age = db.Column(db.Float, nullable=False)

    def __init__(self, Net_Wealth, Annual_Income, Age, user_name):
        self.Net_Wealth = Net_Wealth
        self.Annual_Income = Annual_Income
        self.Age = Age
        self.user_name = user_name


class User(db.Model, UserMixin):
    """
    User Class
    """

    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProjectForm(FlaskForm):
    Net_Wealth = FloatField('Net Wealth:', validators=[DataRequired()])
    Annual_Income = FloatField('Annual Income', validators=[DataRequired()])
    Age = FloatField('Age:', validators=[DataRequired()])
    username = StringField('Username:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LogInForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')

db.create_all()
db.session.commit()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
