from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatdata.db'
db.init_app(app)


class ChatData(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String, nullable=False)
    user_chat_id = db.Column(db.Integer, nullable=False)
    user_chat_text = db.Column(db.String, nullable=False)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/enter', methods=['POST'])
def enter():
    if request.method == "POST":
        username = request.form['username']
        send_data = ChatData(username=username)
        db.session.add(send_data)
        db.session.commit()
        return redirect(f"/chat/{username}")
    return redirect("/")


@app.route('/chat/<name>')
def chat(name):
    username = name
    data = ChatData.query.filter_by(username=username).first()
    if data is None:
        return redirect("/")
    alldata = ChatData.query.all()
    return render_template("chat.html", username=username, alldata=alldata)


@app.route('/chat/<name>/send', methods=['POST'])
def chat_send(name):
    username = name
    if request.method == "POST":
        chat_text = request.form['chat']
        send_data = ChatData(user_chat_text=chat_text, username=username)
        db.session.add(send_data)
        db.session.commit()
    return redirect(f"/chat/{username}")


if __name__ == "__main__":
    app.run(debug=True, port=10)
