from flask import Flask, session, redirect, url_for, escape, request, render_template
from User import User

users = []                              # Users List

admin = User('admin', 'haxxor')      # User Object
users.append(admin)                  # Adding user object to list
users.append(User('test', '123'))    # Adding another uyser

app = Flask(__name__)


@app.route('/',  methods=['GET'])
def index():
    return render_template('index.html', name=session.get('username', ''))


@app.route('/login', methods=['POST'])
def login_action():
    myUser = request.form['username']
    myPass = request.form['password']

    for current_user in users:
        if myUser == current_user.name and myPass == current_user.password:
            session['username'] = myUser
            return redirect(url_for('index'))

    return redirect(url_for('login', error='Wrong user or password'))


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', error=request.args.get('error', None))


@app.route('/logout',  methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if '__main__' == __name__:
    app.run(debug=True)
