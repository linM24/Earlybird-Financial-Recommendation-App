from app import application, classes, db
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, login_required, logout_user
import numpy as np
import pandas as pd
import boto3
import requests

from flask_bootstrap import Bootstrap
from app.candlestick import plotly_candle
import yfinance as yf


@application.route('/index')
@application.route('/')
def index():

   return render_template('index.html', authenticated_user=current_user.is_authenticated)


@application.route('/register', methods=('GET', 'POST'))
def register():
    registration_form = classes.RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data
        email = registration_form.email.data

        user_count = classes.Investor.query.filter_by(username=username).count() + classes.Investor.query.filter_by(email=email).count()
        if (user_count == 0):
            user = classes.Investor(username, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash('Username or Email already exist!')

    return render_template('register.html', form=registration_form)

@application.route('/about', methods=['GET', 'POST'])
def about():

    return render_template('about.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
    login_form = classes.LogInForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # Look for it in the database.
        user = classes.Investor.query.filter_by(username=username).first()
        q_user = classes.Question.query.filter_by(username=username).first()

        # Login and validate the user.
        if user is not None and user.check_password(password):
            login_user(user)
            if q_user is not None:
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('question'))
        else:
            flash('Invalid username and password combination!')

    return render_template('login.html', form=login_form)


@application.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    q5 = 0
    q6 = 0
    q7 = 0
    q8 = 0
    q9 = 0
    q10 = 0
    score = 0

    question_form = classes.QuestionForm()
    if question_form.validate_on_submit():
        username = current_user.username

        age = question_form.age.data
        if int(age)>=18 & int(age)<22:
            q1 = 10
        elif int(age)>=22 & int(age)<26:
            q1 = 7.5
        elif int(age)>=26 & int(age)<30:
            q1 = 5
        else:
            q1 = 2.5

        num_income_source = question_form.num_income_source.data
        if num_income_source =='1':
            q2 = 2.5
        elif num_income_source == '2':
            q2 = 5
        elif num_income_source == '3':
            q2 = 7.5
        else:
            q2 = 10

        marriage = question_form.marriage.data
        if marriage == 'Single':
            q3 = 5
        else:
            q3 = 10

        household = question_form.household.data
        if household == 'R':
            q4 = 5
        else:
            q4 = 10

        mortgage_loan = question_form.mortgage_loan.data
        if mortgage_loan == 'N':
            q5 = 10
        else:
            q5 = 5

        investment_horizon = question_form.investment_horizon.data
        if investment_horizon <= 5:
            q6 = 2.5
        elif investment_horizon >5 & investment_horizon <=7:
            q6 = 5
        elif investment_horizon > 7 & investment_horizon <=10:
            q6 = 7.5
        else:
            q6 = 10

        yearly_income = question_form.yearly_income.data
        if yearly_income == '1':
            q7 = 0
        elif yearly_income =='2':
            q7 = 2
        elif yearly_income == '3':
            q7 = 4
        elif yearly_income =='4':
            q7 = 6
        elif yearly_income == '5':
            q7 = 8
        else:
            q7 = 10

        monthly_expense = question_form.monthly_expense.data
        if monthly_expense == '1':
            q8 = 10
        elif monthly_expense == '2':
            q8 = 8
        elif monthly_expense == '3':
            q8 =6
        elif monthly_expense == '4':
            q8 = 4
        else:
            q8 = 2

        knowledge = question_form.knowledge.data
        if knowledge == '1':
            q9 = 10
        elif knowledge == '2':
            q9 = 7.5
        elif knowledge == '3':
            q9 = 5
        else:
            q9 = 2.5

        aum = question_form.aum.data
        if aum == '1':
            q10 = 2
        elif aum == '2':
            q10 = 4
        elif aum == '3':
            q10 = 6
        elif aum == '4':
            q10 = 8
        elif aum == '5':
            q10 = 10

        score = q1+q2+q3+q4+q5+q6+q7+q8+q9+q10

        info = classes.Question(username, age, num_income_source, marriage, household, mortgage_loan, investment_horizon, yearly_income, monthly_expense, aum, knowledge, score)
        db.session.add(info)
        db.session.commit()
        return redirect(url_for('score'))

    return render_template('question.html', form=question_form, authenticated_user=current_user.is_authenticated)


@application.route('/example')
def example():

   return render_template('example.html')


@application.route('/dashboard')
@login_required
def dashboard():
    ##### cluster
    # assign cluster
    username = current_user.username
    score = classes.Question.query.filter_by(username=username).first().score  # 25, 45, 60, 75, 90
    cluster = None
    if score > 25 and score <= 45:
        cluster = 0
    elif score > 45 and score <= 60:
        cluster = 3
    elif score > 60 and score <= 75:
        cluster = 4
    elif score > 75 and score <= 90:
        cluster = 2
    else:
        cluster = 1

    # fetch cluster data from S3
    bucket = "earlybird-data"
    file_name = f"final/nasdaq_cluster_v1.csv"

    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=bucket, Key=file_name)
    df = pd.read_csv(obj["Body"])

    # some processing steps
    pool = df.loc[df.cluster == cluster]
    first = pool.sort_values(by="returns", ascending=False).iloc[0][["symbol", "company"]]
    pool["returns"] = pool["returns"].apply(lambda x: f"{np.round(100*x, 1)}%")
    pool["volatility"] = pool["volatility"].apply(lambda x: f"{np.round(100 * x, 1)}%")
    profile = pool.profile.iloc[0]
    recommend = pool.sample(5)

    ##### main plot
    company = first["company"]
    ohlc = yf.download(first["symbol"], period="1y").reset_index()
    output = plotly_candle(ohlc)

    ##### sector
    performance = requests.get(f"https://financialmodelingprep.com/api/v3/stock/sectors-performance").json()
    performance = performance["sectorPerformance"]
    dict_sector = {}
    dict_sector["sector"] = [d["sector"] for d in performance]
    dict_sector["change"] = [d["changesPercentage"] for d in performance]
    df_sector = pd.DataFrame(dict_sector)
    df_sector["change"] = df_sector["change"].apply(lambda x: float(x.strip("%")))
    df_sector = df_sector.sort_values(by="change", ascending=False).reset_index(drop=True)
    sector = df_sector.sector.tolist()
    change = df_sector.change.tolist()

    return render_template('dashboard.html', data=recommend, profile=profile, sector=sector, change=change,
                           score=score, source=output, company=company)


@application.route('/score', methods=['GET', 'POST'])
def score():
    info = classes.Question.query.order_by("id").all()
    score = info[-1].score
    return render_template('score.html', score = score)


@application.route('/logout')
def logout():
    before_logout = '<h1> Before logout - is_autheticated : ' \
                    + str(current_user.is_authenticated) + '</h1>'

    logout_user()

    after_logout = '<h1> After logout - is_autheticated : ' \
                   + str(current_user.is_authenticated) + '</h1>'
    #return before_logout + after_logout
    return redirect(url_for('index'))
