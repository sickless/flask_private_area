import os.path
import datetime
from functools import wraps
import sqlite3

from flask import (
    Flask,
    make_response,
    request,
    redirect,
    url_for,
    render_template,
    flash,
    g,
)
from flask_autoindex import AutoIndex
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.config.from_object('config')
idx = AutoIndex(app, app.config['ROOT_PATH'], add_url_rules=False)


def get_db():
    db = getattr(g, '_user_db', None)
    if db is None:
        db = g._user_db = sqlite3.connect(app.config['DATABASE'])
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_user_db', None)
    if db is not None:
        db.close()


def check_password(username, password):
    """Returns bool"""
    db = get_db()
    cur = db.execute('SELECT password FROM user WHERE username = ?', [username])
    salt_password = cur.fetchone()
    if not salt_password:
        return False
    return check_password_hash(salt_password[0], password)


def get_expire_date():
    """Returns datetime"""
    expire_date = datetime.datetime.utcnow()
    expire_date += datetime.timedelta(seconds=app.config['COOKIE_DURATION'])
    return expire_date


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (request.cookies.get(app.config['COOKIE_NAME']) !=
            app.config['COOKIE_VALUE']):
            return redirect(url_for('login', next=request.url))
        response = make_response(f(*args, **kwargs))
        # When the cookie is still valid, re-update the cookie's expiration date
        response.set_cookie(app.config['COOKIE_NAME'],
            app.config['COOKIE_VALUE'], expires=get_expire_date())
        return response
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        if check_password(username, password):
            response = make_response(redirect(request.args.get('next')))
            response.set_cookie(app.config['COOKIE_NAME'],
                app.config['COOKIE_VALUE'], expires=get_expire_date())
            return response
        else:
            flash('Invalid credentials', 'error_logging')
    return render_template('login.html')


@app.route('/')
@app.route('/<path:path>')
@login_required
def autoindex(path='.'):
    root_path = app.config['ROOT_PATH']
    if (os.path.isdir(os.path.join(root_path, path)) and
        os.path.isfile(os.path.join(root_path, path, 'index.html'))):
        # Path is a directory which contains an index.html file, render it
        return redirect(os.path.join(path, 'index.html'))
    return idx.render_autoindex(path)


if __name__ == '__main__':
    app.run()
