from os import getenv

from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)





#
#   index and logging in
#
@app.route("/")
def index():
    return render_template("index.html")



@app.route("/new_user")
def new_user():
    return render_template("new_user.html")


@app.route("/new_user/submit", methods=["POST"])
def new_user_submit():
    if (request.form["password1"] != request.form["password2"]):
        return "Passwords must be same"
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username": request.form["username"], "password": request.form["password1"]})
    db.session.commit()
    print(request.form)
    return redirect("/")


@app.route("/login/submit", methods=["POST"])
def login_submit():
    username = request.form["username"]
    password = request.form["password"]
    session["username"] = username
    return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")



#
#   Teachers
#

@app.route("/teachers")
def teachers():
    return render_template("teachers.html")
