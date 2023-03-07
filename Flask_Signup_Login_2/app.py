from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy()
db.init_app(app)
app.secret_key = '\xf9VB\xec\xb8\x17\xedt\xc5\t\xf6\xd3g\xec\xa2\x19k\xf4\x03\x92Z:\x11\x9a'


class DATABASE(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


@app.route('/')
def Home():
    if 'username' in session:
        username = session['username']
        alldata = DATABASE.query.filter_by(username=username).first()
        name = alldata.name
        return render_template("index.html", username=username, name=name)
    else:
        return redirect(url_for('LogIn'))


@app.route('/login')
def LogIn():
    if 'username' in session:
        return redirect(url_for('Home'))
    return render_template("login.html")


@app.route('/signup')
def SignUp():
    if 'username' in session:
        return redirect(url_for('Home'))
    return render_template("signup.html")


@app.route('/login/action', methods=['POST'])
def LogIn_Action():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            getdata = DATABASE.query.filter_by(username=username).first()
            pas = getdata.password
            decrypted_password = check_password_hash(pas, password)
            if decrypted_password:
                session['username'] = username
                return redirect(url_for('Home'))
            else:
                return redirect(url_for('LogIn'))
        except:
            return redirect(url_for('LogIn'))
    else:
        return redirect(url_for('LogIn'))


@app.route('/signup/action', methods=['POST'])
def SignUp_Action():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        encrypted_password = generate_password_hash(password)
        senddata = DATABASE(name=name, username=username, email=email, password=encrypted_password)
        db.session.add(senddata)
        db.session.commit()
        return redirect(url_for('LogIn'))
    else:
        return redirect(url_for('SignUp'))


@app.route('/logout', methods=['POST', 'GET'])
def LogOut():
    if request.method == 'POST':
        session.pop('username')
        return redirect(url_for('LogIn'))
    if request.method == 'GET':
        return redirect(url_for('Home'))


if __name__ == '__main__':
    app.run(debug=True, port=10)