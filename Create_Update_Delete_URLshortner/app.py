from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random as rd, string

app = Flask(__name__)

db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///URL_DATA.db'
db.init_app(app)


class URL_DATA(db.Model):
    url_id = db.Column(db.Integer, primary_key=True, unique=True)
    web_url = db.Column(db.String, nullable=False)
    short_url = db.Column(db.String, nullable=False)
    url_title = db.Column(db.String, nullable=False)


@app.route('/')
def home():
    alldata = URL_DATA.query.all()
    site_url = request.base_url
    return render_template("index.html", alldata=alldata, site_url=site_url)


@app.route('/<name>')
def shorturl(name):
    alldata = URL_DATA.query.filter_by(short_url=name).first()
    return redirect(alldata.web_url)


@app.route('/delete/<name>')
def delete(name):
    alldata = URL_DATA.query.filter_by(short_url=name).first()
    db.session.delete(alldata)
    db.session.commit()
    return redirect("/")


@app.route('/update/<name>')
def update(name):
    alldata = URL_DATA.query.filter_by(short_url=name).first()
    return render_template("update.html", alldata=alldata)


@app.route('/update/<name>/done', methods=['POST'])
def update_process(name):
    if request.method == "POST":
        web_url = request.form['url']
        short_url = request.form['short url']
        url_title = request.form['title']
        alldata = URL_DATA.query.filter_by(short_url=name).first()
        alldata.web_url = web_url
        alldata.short_url = short_url
        alldata.url_title = url_title
        db.session.add(alldata)
        db.session.commit()
    return redirect("/")


@app.route('/create', methods=['POST'])
def create():
    if request.method == "POST":
        url = request.form['url']
        title = request.form['title']
        letters = string.ascii_letters + string.digits
        short_url = "".join(rd.choice(letters) for _ in range(10))
        data = URL_DATA(web_url=url, url_title=title, short_url=short_url)
        db.session.add(data)
        db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=10)