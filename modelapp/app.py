from flask import Flask, session, redirect, url_for, request, render_template, flash
from models.user import db, User
from os import makedirs, path

app = Flask(__name__)
app.config.update(dict(SQLALCHEMY_DATABASE_URI='sqlite:///./db/db.sqlite3'))
app.config.update(dict(SQLALCHEMY_TRACK_MODIFICATIONS=False))

if not path.exists('./db'):
    makedirs('./db')

db.init_app(app)
db.create_all(app=app)

user = User()

@app.route('/')
def index():
    return render_template('index.html', name=session.get('username', ''))


@app.route('/login', methods=['POST'])
def login_action():
    if user.checkUser(request.form['username'], request.form['password']):
        session['username'] = request.form['username']
        flash('Login successfull')
        return redirect(url_for('index'))

    flash('Login failed')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)   
    flash('Logout successfull')
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register_action():
    if not user.addUser(request.form['username'], request.form['password']):
        flash('Registration failed')
        return redirect(url_for('register'))
    
    flash('Registration successfull')
    return redirect(url_for('login'))

@app.route('/register')
def register():
    return render_template('register.html')

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if '__main__' == __name__:
    app.run(debug=True)
