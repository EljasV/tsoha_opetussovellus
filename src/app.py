from os import getenv

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/page/<int:id>")
def page(id):
    return "Tämä on sivu " + str(id)


@app.route("/new_user")
def new_user():
    return render_template("new_user.html")


@app.route("/new_user/submit", methods=["POST"])
def new_user_submit():
    if (request.form["password1"] != request.form["password2"]):
        return "Passwords must be same"
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username": request.form["username"], "password": request.form["password1"]})
    print(request.form)
    return redirect("/")
