from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def login():
    error = ''

    if request.method == 'POST':
        user = request.form['user']
        passwd = request.form['passwd']

        if check(user,passwd):
            return redirect(url_for('success'))
        else:
            error = 'Invalid Credentials'

    return render_template('index.html', error=error)
        
def simple_check(user,passwd):
    if user == 'test' and passwd == '123':
        return True
    else:
        return False
        

def check(user,passwd):
    with open('userdata','r') as f:
        for i,elem in enumerate(f):
            [user_d, passwd_d] = elem.split(':')
            if user == user_d and passwd == passwd_d:                               return True
            else:
               return False

@app.route('/register', methods=['GET','POST'])
def register():
    
    if request.method == 'POST':
        with open('userdata','a') as f:
            f.write('\n'+request.form['user']+':'+request.form['passwd'])

    return render_template('register.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    login()
