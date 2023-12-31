from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"

db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno}: {self.title}"

@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form["title"]
        desc = request.form['description']
        todo = ToDo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()

    allTodos = ToDo.query.all()
    return render_template('index.html', allTodos = allTodos)

@app.route("/update/<int:srno>", methods = ['GET', 'POST'])
def update(srno):
    if request.method == 'POST':
        title = request.form["title"]
        desc = request.form['description']
        todo = ToDo.query.filter_by(sno = srno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    updateTodo = ToDo.query.filter_by(sno = srno).first()
    return render_template("update.html", todo = updateTodo)

@app.route("/delete/<int:srno>")
def delete(srno):
    deleteTodo = ToDo.query.filter_by(sno = srno).first()
    db.session.delete(deleteTodo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)