from flask import Flask, session, redirect, url_for, escape, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', name=session.get('username', ''))


@app.route('/login', methods=['POST'])
def login_action():
    session['username'] = request.form['username']
    return redirect(url_for('index'))


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if '__main__' == __name__:
    app.run(debug=True)
