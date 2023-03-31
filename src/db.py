from os import getenv

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db = SQLAlchemy(app)


def create_new_user(username: str, password: str):
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password) RETURNING id")
    r = db.session.execute(sql, {"username": username, "password": password})
    db.session.commit()
    return r.fetchone()[0]


def get_user_by_username(username):
    sql = text("SELECT * FROM users WHERE username=:username")
    r = db.session.execute(sql, {"username": username})
    return r.fetchone()


def add_new_course(course_name: str, course_description: str):
    sql = text("INSERT INTO courses (course_name, description) VALUES (:course_name, :description) RETURNING id")
    r = db.session.execute(sql, {"course_name": course_name, "description": course_description})
    db.session.commit()
    return r.fetchone()[0]


def add_course_teacher(teacher_id: int, course_id: int):
    sql = text("INSERT INTO course_teachers (teacher_id, course_id) VALUES (:teacher_id, :course_id) RETURNING id")
    r = db.session.execute(sql, {"teacher_id": teacher_id, "course_id": course_id})
    db.session.commit()
    return r.fetchone()[0]


def get_teachers_courses(username):
    sql = text(
        "SELECT C.id, C.course_name, C.description FROM courses C, course_teachers CT, users U WHERE CT.course_id = C.id AND CT.teacher_id = U.id AND U.username = :username")
    r = db.session.execute(sql, {"username": username})
    return r.fetchall()
