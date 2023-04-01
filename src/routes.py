import db
from app import app

from flask import render_template, request, redirect, session

from db import create_new_user


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
    create_new_user(request.form["username"], request.form["password1"])
    return redirect("/")


@app.route("/login/submit", methods=["POST"])
def login_submit():
    username = request.form["username"]
    password = request.form["password"]

    user = db.get_user_by_username(username)

    if user is None or user[2] != password:
        return redirect("/")

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


@app.route("/teachers/create_course")
def teachers_create_course():
    return render_template("teachers/create_course.html")


@app.route("/teachers/create_course/submit", methods=["POST"])
def teachers_create_course_submit():
    course = db.add_new_course(request.form["course_name"], request.form["description"])

    teacher = db.get_user_by_username(session["username"])[0]

    db.add_course_teacher(teacher, course)

    return redirect("/teachers")


@app.route("/teachers/my_courses")
def teacher_my_courses():
    courses = []

    teachers_courses = db.get_teachers_courses(session["username"])

    for course in teachers_courses:
        courses.append({"course_id": course[0], "course_name": course[1], "description": course[2]})
    return render_template("teachers/my_courses.html", courses=courses)


@app.route("/teachers/courses/<int:id>")
def teacher_courses_id(id: int):
    course = db.get_course_by_id(id)

    chapters = []
    fetched_chapters = db.get_courses_chapters(id)

    for chapter in fetched_chapters:
        chapters.append({"name": chapter[2]})

    return render_template("teachers/courses_id.html", name=course[1], description=course[2], chapters=chapters)
