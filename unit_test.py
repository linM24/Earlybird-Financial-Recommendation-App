from app import classes, application, db
from werkzeug.security import check_password_hash, generate_password_hash
from data_acquisition import cluster


# def test_colname():
# 	user_colname = []
# 	project_colname = []
# 	for i in classes.User.__table__.columns:
# 		user_colname.append(i)
# 	for i in classes.Project.__table__.columns:
# 		project_colname.append(i)
#
# 	assert user_colname == ['id','username','email','password_hash']
# 	assert project_colname == ['id','user_name','Net_Wealth','Annual_Income','Age']


def test_question():
	"""
	Test whether user has the questionnaire input correctly specified
	"""
	assert classes.Question.query.first().age >= 22
	assert classes.Question.query.first().gender in ["F", "M"]
	assert classes.Question.query.first().marriage in ["Single", "Married"]
	assert classes.Question.query.first().household in ["H", "R"]
	assert classes.Question.query.first().mortgage_loan in ["Y", "N"]
	assert classes.Question.query.first().investment_horizen >= 0
	assert classes.Question.query.first().yearly_income in [str(i) for i in range(1, 7)]
	assert classes.Question.query.first().monthly_expense in [str(i) for i in range(1, 6)]


def test_user():
	# Assuming that "ddd, d@gmail.com, 1234" is always in the database
	assert classes.Investor.query.filter_by(username='ddd').first().email == 'd@gmail.com'
	assert classes.Investor.query.filter_by(username='ddd').first().username == 'ddd'
	assert check_password_hash(classes.Investor.query.filter_by(username='ddd').first().password_hash, "1234")


def test_cluster():
	"""
	Test the tentative clusters have the correct number of recommendations
	"""
	dict_ = {}
	for i in cluster.kmeans.labels_:
		dict_[i] = dict_.get(i, 0) + 1
	assert len(dict_.keys()) == 9
	assert cluster.cluster0.shape[0] == 20
	assert cluster.cluster1.shape[0] == 20
	assert cluster.cluster2.shape[0] == 20
	assert cluster.cluster3.shape[0] == 20