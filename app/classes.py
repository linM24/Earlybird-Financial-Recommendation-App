from flask_login import UserMixin
from flask_wtf import FlaskForm

from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import DateField, IntegerField, PasswordField, SelectField, StringField, SubmitField, FloatField
from wtforms.validators import DataRequired

from app import db, login_manager


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    num_income_source = db.Column(db.Integer, nullable=False)
    marriage = db.Column(db.String(80), nullable=False)
    household = db.Column(db.String(80), nullable=False)
    mortgage_loan = db.Column(db.String(80), nullable=False)
    investment_horizen = db.Column(db.Integer, nullable=False)
    yearly_income = db.Column(db.String(80), nullable=False)
    monthly_expense = db.Column(db.String(80), nullable=False)
    aum = db.Column(db.String(80), nullable=False)
    knowledge = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Float, nullable=False)

    def __init__(self, username, age, num_income_source, marriage, household, mortgage_loan, investment_horizon, yearly_income, monthly_expense,aum, knowledge, score):
        self.username = username
        self.age = age
        self.num_income_source = num_income_source
        self.marriage = marriage
        self.household = household
        self.mortgage_loan = mortgage_loan
        self.investment_horizen =  investment_horizon
        self.yearly_income = yearly_income
        self.monthly_expense = monthly_expense
        self.aum = aum
        self.knowledge = knowledge
        self.score = score


class Investor(db.Model, UserMixin):
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


class QuestionForm(FlaskForm):
    age = IntegerField('What is your age:', validators=[DataRequired()])
    num_income_source = SelectField('How many source of income do you have?', choices=[('1', '1'), ('2', '2'),
                                                   ('3', '3'), ('4', '4&up')])
    marriage = SelectField('Please select your marriage status', choices=[('Single', 'Single'), ('Married', 'Married')])
    household = SelectField('Do you own a house or rent the apartment?', choices=[('H', 'Own House'), ('R', 'Rent Apartment')])
    mortgage_loan = SelectField('Do you carry mortgage loan', choices=[('Y', 'Yes'), ('N', 'No')])
    investment_horizon = IntegerField('What is your investment horizon:', validators=[DataRequired()])
    yearly_income=SelectField('What is your annual income', choices=[('1', '30,000-70,000'), ('2', '70,000-100,000'),
                                                   ('3', '100,000-130,000'), ('4', '130,000-160,000'),
                                                   ('5', '160,000-200,000'), ('6', '200,000-240,000'),
                                                   ('3', '100,000-130,000') ])
    monthly_expense = SelectField('What is your monthly expense', choices=[('1', '500-1,000'), ('2', '1,000-2,500'),
                                                   ('3', '2,500-4,000'), ('4', '4,000-5,500'),
                                                   ('5', '5,500&up') ])
    aum = SelectField('What is your AUM(asset under managment) amount for this portfolio? ', choices=[('1', 'below 10k'), ('2', '10k-25k'),
                                                   ('3', '25k-40k'), ('4', '40k-60k'),
                                                   ('5', '60k&more') ])
    knowledge = SelectField('Do you have any basic knowledge of financial instrument? ', choices=[('1', 'Yes, master level! You have over 3 years finance related working experience or have a bachelor degree with business related major'),
                                                                                                  ('2', 'Yes, intermediate level. You have investment experience and understand the risk of financial instrument'),
                                                                                                ('3', 'Yes, entry level. You have limit knowledge of what financial instrument is.'),
                                                                                                ('4', 'No,novice level. You are curious to learn the basic knowledge of financial instrument')])
    submit = SubmitField('Submit')


class LogInForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')


db.create_all()
db.session.commit()


@login_manager.user_loader
def load_user(id):
    return Investor.query.get(int(id))
