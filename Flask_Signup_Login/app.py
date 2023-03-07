from flask import Flask, render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy()
db.init_app(app)
app.secret_key = 'ksdjflskdjfsfkdfjdk'


class DATABASE(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_full_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=False)


# route for home page
@app.route('/')
def Home():
    if 'username' in session:
        username = session['username']
        return render_template("index.html", username=username)
    else:
        return redirect(url_for("LogIn"))


# route for signup page
@app.route('/signup')
def SignUP():
    if 'username' in session:
        return redirect(url_for('Home'))
    return render_template("signup.html")


# route for login page
@app.route('/login')
def LogIn():
    if 'username' in session:
        return redirect(url_for('Home'))
    return render_template("login.html")


# route for signup action page
@app.route('/signup/action', methods=['POST'])
def SignUp_Action():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        senddata = DATABASE(user_full_name=name, username=username, email=email, password=password)
        db.session.add(senddata)
        db.session.commit()
        return redirect(url_for('LogIn'))
    if 'username' in session:
        return redirect(url_for('Home'))
    return redirect(url_for('SignUp'))


# route for login action page
@app.route('/login/action', methods=['POST'])
def LogIn_Action():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        getdata = DATABASE.query.filter_by(username=username, password=password).first()
        if getdata:
            session['username'] = username
            return redirect(url_for('Home'))
    if 'username' in session:
        return redirect(url_for('Home'))
    return redirect(url_for('LogIn'))


@app.route('/logout')
def LogOut():
    session.pop('username')
    return redirect(url_for('LogIn'))


if __name__ == "__main__":
    app.run(debug=True, port=10)
