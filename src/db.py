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


def get_user_by_username(username: str):
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


def get_teachers_courses(username: str):
    sql = text(
        "SELECT C.id, C.course_name, C.description FROM courses C, course_teachers CT, users U WHERE CT.course_id = C.id AND CT.teacher_id = U.id AND U.username = :username")
    r = db.session.execute(sql, {"username": username})
    return r.fetchall()


def get_course_by_id(id: int):
    sql = text("SELECT * FROM courses WHERE id=:id")
    r = db.session.execute(sql, {"id": id})
    return r.fetchone()


def get_courses_chapters(id: int):
    sql = text("SELECT * FROM course_chapters WHERE course_id=:id")
    r = db.session.execute(sql, {"id": id})
    return r.fetchall()


def check_if_username_exists(username: str):
    sql = text("SELECT 1 FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    return bool(result.fetchone())


def add_course_chapter(course_id: int, chapter_name: str, chapter_content: str):
    sql = text(
        "INSERT INTO course_chapters (course_id, chapter_name, chapter_content) VALUES (:course_id, :chapter_name, :chapter_content)")
    result = db.session.execute(sql, {"course_id": course_id, "chapter_name": chapter_name,
                                      "chapter_content": chapter_content})
    db.session.commit()


def add_course_teacher_by_username(teacher_name: str, course_id: int):
    sql = text(
        "INSERT INTO course_teachers (teacher_id, course_id) VALUES ((SELECT id FROM users WHERE username=:teacher_name), :course_id) RETURNING id")
    r = db.session.execute(sql, {"teacher_name": teacher_name, "course_id": course_id})
    db.session.commit()
    return r.fetchone()[0]


def get_course_teachers(course_id: int):
    sql = text(
        "SELECT U.id, U.username FROM course_teachers CT, users U WHERE CT.course_id = :course_id AND CT.teacher_id = U.id")
    r = db.session.execute(sql, {"course_id": course_id})
    return r.fetchall()


def get_chapter_by_id(chapter_id: int):
    sql = text("SELECT * FROM course_chapters WHERE id=:chapter_id")
    r = db.session.execute(sql, {"chapter_id": chapter_id})
    return r.fetchone()


def create_new_exercise(chapter_id: int, exercise_question: str):
    sql = text("INSERT INTO chapter_exercises (chapter_id, question, correct_answer) VALUES (:chapter_id,:question,-1)")
    r = db.session.execute(sql, {"chapter_id": chapter_id, "question": exercise_question})
    db.session.commit()


def get_chapter_exercises_and_answers(chapter_id: int):
    sql = text(
        "SELECT  EX.*, json_agg( OPT.*) FROM chapter_exercises EX LEFT JOIN exercise_options OPT ON EX.id = OPT.exercise WHERE EX.chapter_id = :chapter_id GROUP BY EX.id")
    r = db.session.execute(sql, {"chapter_id": chapter_id})
    return r.fetchall()


def get_student_exercises_for_chapter(student_id: int, chapter_id: int):
    sql = text(
        "SELECT EX.*, json_agg(DISTINCT OPT.*), json_agg(DISTINCT ES.*) FROM chapter_exercises EX LEFT JOIN exercise_options OPT ON EX.id = OPT.exercise LEFT JOIN exercise_submissions ES ON ES.exercise_id=EX.id WHERE EX.chapter_id=:chapter_id AND (ES.student_id=:student_id OR ES.student_id IS NULL) GROUP BY EX.id")
    r = db.session.execute(sql, {"student_id": student_id, "chapter_id": chapter_id})
    return r.fetchall()


def add_exercise_option(exercise_id: int, answer: str):
    sql = text("INSERT INTO exercise_options (answer, exercise) VALUES (:answer, :exercise_id)")
    r = db.session.execute(sql, {"answer": answer, "exercise_id": exercise_id})
    db.session.commit()


def get_exercise_chapter(id: int):
    sql = text("SELECT chapter_id FROM chapter_exercises WHERE id=:id")
    r = db.session.execute(sql, {"id": id})
    return r.fetchone()[0]


def set_exercise_correct(exercise_id: int, option_id: int):
    sql = text("UPDATE chapter_exercises SET correct_answer=:option_id WHERE id=:exercise_id")
    r = db.session.execute(sql, {"exercise_id": exercise_id, "option_id": option_id})
    db.session.commit()


def does_teacher_teach_course(teacher_id: int, course_id: int):
    sql = text("SELECT 1 FROM course_teachers WHERE teacher_id = :teacher_id AND course_id = :course_id")
    r = db.session.execute(sql, {"teacher_id": teacher_id, "course_id": course_id})
    return bool(r.fetchone())


def get_all_courses():
    sql = text("SELECT * FROM courses")
    r = db.session.execute(sql)
    return r.fetchall()


def add_course_student(student_id: int, course_id: int):
    sql = text("INSERT INTO course_students(student_id, course_id) VALUES (:student_id,:course_id)")
    r = db.session.execute(sql, {"student_id": student_id, "course_id": course_id})
    db.session.commit()


def is_student_attending_course(student_id: int, course_id: int):
    sql = text("SELECT 1 FROM course_students WHERE course_id=:course_id AND student_id=:student_id")
    r = db.session.execute(sql, {"course_id": course_id, "student_id": student_id})
    return bool(r.fetchone())


def is_exercise_correct(exercise_id: int, answer_id: int):
    sql = text("SELECT 1 FROM chapter_exercises WHERE id=:exercise_id AND correct_answer=:answer_id")
    r = db.session.execute(sql, {"exercise_id": exercise_id, "answer_id": answer_id})

    return bool(r.fetchone())


def get_students_courses(student_id: int):
    sql = text("SELECT CO.* FROM courses CO, course_students CS WHERE CO.id=CS.course_id AND CS.student_id=:student_id")
    r = db.session.execute(sql, {"student_id": student_id})
    return r.fetchall()


def submit_exercise(student_id: int, exercise_id: int, answered_id: int):
    sql = text(
        "INSERT INTO exercise_submissions (student_id, exercise_id, option_id) VALUES (:student_id, :exercise_id, :option_id)")
    r = db.session.execute(sql, {"student_id": student_id, "exercise_id": exercise_id, "option_id": answered_id})
    db.session.commit()
    return None
