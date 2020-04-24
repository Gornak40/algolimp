from flask import Flask, render_template, url_for, request, session, redirect
from cfApi import userInfo
from random import randint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


interfaces = [
	'name',
	'other',
	'description',
	'urls',
	'paste',
	'user'
]
app = Flask(__name__)
app.config['SECRET_KEY'] = generate_password_hash('Alfred Hitchcock')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/gornak40/code/yandex/algolimp/data/algo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Algo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, unique=True, nullable=False)
	other = db.Column(db.String, nullable=False)
	description = db.Column(db.Text, nullable=False)
	urls = db.Column(db.Text, nullable=False)
	paste = db.Column(db.String)
	user = db.Column(db.String, nullable=False)


@app.route('/')
def index():
	kwargs = dict()
	kwargs['title'] = 'Home'
	kwargs['content_title'] = 'Home'
	return render_template('index.html', **kwargs, **session)


@app.route('/algo/adding/', methods=['post', 'get'])
def adding():
	kwargs = dict()
	kwargs['title'] = 'Adding'
	kwargs['content_title'] = 'Adding'
	if request.method == 'POST':
		session['algo'] = session.get('algo', dict())
		name = request.form.get('name')
		other = request.form.get('other')
		description = request.form.get('description')
		urls = request.form.get('urls')
		paste = request.form.get('paste')
		user = session.get('user')
		if name:
			session['algo']['name'] = name
		if other:
			session['algo']['other'] = other
		if description:
			session['algo']['description'] = description
		if urls:
			session['algo']['urls'] = urls
		if paste:
			session['algo']['paste'] = paste
		session['algo']['user'] = user['handle']
		if (all([session['algo'].get(i) for i in interfaces])):
			# здесь я типо базу данных обновляю
			return redirect('/algo')
	return render_template('adding.html', **kwargs, **session)


@app.route('/algo/', methods=['post', 'get'])
def algo():
	kwargs = dict()
	kwargs['title'] = 'Algo'
	kwargs['content_title'] = 'Algo'
	if request.method == 'POST' and session.get('auth'):
		return redirect('/algo/adding')
	return render_template('algo.html', **kwargs, **session)


@app.route('/login/', methods=['post', 'get'])
def login():
	kwargs = dict()
	kwargs['title'] = 'Login'
	kwargs['content_title'] = 'Login'
	if request.method == 'POST':
		handle = request.form.get('handle')
		code = request.form.get('code')
		if handle:
			session['handle'] = handle
			session['user'] = userInfo(handle)
			session['email'] = session['user'].get('email') if session['user'] else None
			session['secret'] = str(randint(1000, 9999))
			session['auth'] = False
		session['code'] = code if code else str()
		if session['code'] and session['secret'] and session['code'] == session['secret']:
			session['auth'] = True

	return render_template('login.html', **kwargs, **session)


@app.route('/logout/')
def logout():
	kwargs = dict()
	kwargs['title'] = 'Logout'
	kwargs['content_title'] = 'Logout'
	session.clear()
	# session.pop('email') if session.get('email') else None
	# session.pop('code') if session.get('code') else None
	# session.pop('handle') if session.get('handle') else None
	# session.pop('secret') if session.get('secret') else None
	# session.pop('auth') if session.get('auth') else None
	return render_template('logout.html', **kwargs, **session)


if __name__ == '__main__':
	app.run(debug=True)