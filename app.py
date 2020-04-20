from flask import Flask, render_template, url_for, request, session, redirect
from cfApi import userInfo
from random import randint
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = generate_password_hash('Alfred Hitchcock')


@app.route('/')
def index():
	kwargs = dict()
	kwargs['title'] = 'Home'
	kwargs['content_title'] = 'Home'
	return render_template('index.html', **kwargs, **session)


@app.route('/algo/adding/')
def adding():
	kwargs = dict()
	kwargs['title'] = 'Adding'
	kwargs['content_title'] = 'Adding'
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
			info = userInfo(handle)
			session['email'] = info.get('email') if info else None
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
	session.pop('email') if session.get('email') else None
	session.pop('code') if session.get('code') else None
	session.pop('handle') if session.get('handle') else None
	session.pop('secret') if session.get('secret') else None
	session.pop('auth') if session.get('auth') else None
	return render_template('logout.html', **kwargs, **session)


if __name__ == '__main__':
	app.run(debug=True)