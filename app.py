from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return "{}".format(self.title)

@app.route("/", methods=["GET","POST"])
def hello_world():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template("index.html", alltodo=alltodo)

@app.route("/about")
def about_us():
    alltodo = Todo.query.all()
    # this will fetch all the data from database
    print(alltodo)
    return "I'm a python developer"

@app.route("/update/<int:sno>", methods=["GET","POST"])
def update(sno):
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    alltodo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", alltodo=alltodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    alltodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(alltodo)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)