from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///post.db"
db.init_app(app)


class post_data(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(200), nullable=False)
    post_description = db.Column(db.String, nullable=False)


@app.route('/')
def home():
    posts = post_data.query.all()
    title = ["create post"]
    description = ["create post"]
    postlen = len(posts)
    if len(posts) >= 1:
        title = [post.post_title for post in posts]
        description = [post.post_description[0:150] for post in posts]
    return render_template("index.html", title=title, description=description, posts=posts, postlen=postlen)


@app.route('/create-post')
def create_post():
    return render_template("create_post.html")


@app.route('/create-post/post', methods=['POST'])
def upload_post():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        post = post_data(post_title=title, post_description=description)
        db.session.add(post)
        db.session.commit()
        return redirect("/")


@app.route('/post/<name>')
def show_post(name):
    post = post_data.query.all()
    if len(post) >= 1:
        title = " ".join(name.split("-"))
        posts = post_data.query.filter_by(post_title=title)
    return render_template("show_post.html", posts=posts)


@app.route('/my-posts')
def my_posts():
    posts = post_data.query.all()
    if len(posts) == 0:
        return redirect("/")
    return render_template("my_posts.html", posts=posts)


@app.route('/edit-posts/<name>')
def edit_posts(name):
    posts = post_data.query.all()
    if len(posts) == 0:
        return redirect("/")
    return render_template("edit_posts.html", posts=posts)


@app.route('/edit-posts/<name>/update', methods=['POST'])
def update_posts(name):
    posts = post_data.query.all()
    if len(posts) == 0:
        return redirect("/")
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        data = post_data.query.filter_by(post_title=title).first()
        data.post_title = title
        data.post_description = description
        db.session.add(data)
        db.session.commit()

    return redirect("/my-posts")


@app.route('/delete/<name>')
def delete_posts(name):
    post = post_data.query.all()
    if len(post) >= 1:
        title = " ".join(name.split("-"))
        posts = post_data.query.filter_by(post_title=title).first()
        db.session.delete(posts)
        db.session.commit()
    return redirect("/my-posts")


if __name__ == "__main__":
    app.run(debug=True, port=10)
