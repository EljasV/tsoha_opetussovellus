from flask import render_template, request, redirect, session, abort

import db
from app import app


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
    username = request.form["username"]
    if len(username) < 2:
        return "Username must be at least 2 characters long"
    if db.check_if_username_exists(username):
        return "Username exists already"
    if len(request.form["password1"]) < 5:
        return "Password must be at least 7 characters long"
    if request.form["password1"] != request.form["password2"]:
        return "Passwords must be same"

    db.create_new_user(username, request.form["password1"])
    return redirect("/")


@app.route("/login/submit", methods=["POST"])
def login_submit():
    username = request.form["username"]
    password = request.form["password"]

    user = db.get_user_by_username(username)

    if user is None or user[2] != password:
        return redirect("/")

    session["username"] = username
    session["userid"] = user[0]
    return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    del session["userid"]
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
    course_name = request.form["course_name"]
    course_description = request.form["description"]

    if course_name == "":
        return "Course must have a name"
    if course_description == "":
        return "Course must have a description"

    course = db.add_new_course(course_name, course_description)

    teacher = session["userid"]

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
        chapters.append({"name": chapter[2], "id": chapter[0]})

    teachers = []
    fetcherd_teachers = db.get_course_teachers(id)

    for teacher in fetcherd_teachers:
        teachers.append({"name": teacher[1]})

    return render_template("teachers/courses_id.html", name=course[1], description=course[2], chapters=chapters, id=id,
                           teachers=teachers)


@app.route("/teachers/courses/<int:id>/submit_chapter", methods=["POST"])
def teacher_courses_add_chapter(id: int):
    if not session["userid"] or not db.does_teacher_teach_course(session["userid"], id):
        return "You must be a teacher in the course"

    chapter_name = request.form["chapter_name"]
    chapter_content = request.form["chapter_content"]
    db.add_course_chapter(id, chapter_name, chapter_content)
    return redirect("/teachers/courses/" + str(id))


@app.route("/teachers/courses/<int:id>/add_course_teacher", methods=["POST"])
def teacher_courses_add_teacher(id: int):
    if not session["userid"] or not db.does_teacher_teach_course(session["userid"], id):
        return "You must be a teacher in the course"

    teacher_name = request.form["teacher_name"]
    if not db.check_if_username_exists(teacher_name):
        return "Teacher must exist"
    db.add_course_teacher_by_username(teacher_name, id)
    return redirect("/teachers/courses/" + str(id))


@app.route("/teachers/chapters/<int:id>")
def teacher_chapters_id(id: int):
    chapter = db.get_chapter_by_id(id)
    if not chapter:
        return abort(404)
    fetched_course = db.get_course_by_id(chapter[1])
    course = {"id": fetched_course[0], "name": fetched_course[1]}
    exercises = db.get_chapter_exercises_and_answers(id)

    return render_template("teachers/chapters_id.html", id=id, name=chapter[2], content=chapter[3], course=course,
                           exercises=exercises.values())


@app.route("/teachers/chapters/<int:id>/submit_new_exercise", methods=["POST"])
def teachers_chapters_submit_new_exercise(id: int):
    course_id = db.get_chapter_by_id(id)[1]

    if not session["userid"] or not db.does_teacher_teach_course(session["userid"], course_id):
        return "You must be a teacher in the course"

    exercise_question = request.form["exercise_question"]
    db.create_new_exercise(id, exercise_question)
    return redirect("/teachers/chapters/" + str(id))


@app.route("/teachers/exercises/<int:id>/submit_new_option", methods=["POST"])
def teachers_exercises_submit_new_option(id: int):
    chapter_id = db.get_exercise_chapter(id)
    course_id = db.get_chapter_by_id(id)[1]

    if not session["userid"] or not db.does_teacher_teach_course(session["userid"], course_id):
        return "You must be a teacher in the course"

    answer = request.form["answer"]
    db.add_exercise_option(id, answer)
    return redirect("/teachers/chapters/" + str(chapter_id))


@app.route("/teachers/exercises/<int:exercise_id>/set_correct/<int:option_id>")
def teachers_exercises_set_correct(exercise_id: int, option_id: int):
    chapter_id = db.get_exercise_chapter(exercise_id)
    course_id = db.get_chapter_by_id(chapter_id)[1]

    if not session["userid"] or not db.does_teacher_teach_course(session["userid"], course_id):
        return "You must be a teacher in the course"

    db.set_exercise_correct(exercise_id, option_id)
    return redirect("/teachers/chapters/" + str(chapter_id))


#
#   Students
#

@app.route("/students")
def students():
    return render_template("students.html")


@app.route("/students/my_courses")
def students_my_courses():
    return render_template("students/my_courses.html")


@app.route("/students/all_courses")
def students_all_courses():
    fetched_courses = db.get_all_courses()
    courses = []
    for course in fetched_courses:
        courses.append({"course_id": course[0], "course_name": course[1], "description": course[2]})

    return render_template("students/all_courses.html", courses=courses)


@app.route("/students/courses/<int:id>")
def students_courses_id(id: int):
    student_id = session["userid"]
    if student_id:
        attending = db.is_student_attending_course(student_id, id)
    else:
        attending = False

    fetched_teachers = db.get_course_teachers(id)

    teachers = []
    for teacher in fetched_teachers:
        teachers.append({"name": teacher[1]})

    fetched_chapters = db.get_courses_chapters(id)
    chapters = []

    for chapter in fetched_chapters:
        chapters.append({"name": chapter[2], "id": chapter[0]})

    return render_template("students/courses_id.html", attending=attending, id=id, teachers=teachers, chapters=chapters)


@app.route("/students/courses/<int:course_id>/join", methods=["POST"])
def students_courses_join(course_id: int):
    student_id = session["userid"]
    if not student_id:
        return "You must be logged in in order to join the course"
    db.add_course_student(student_id, course_id)
    return redirect("/students/courses/" + str(course_id))


@app.route("/students/chapters/<int:id>")
def students_chapters(id: int):
    chapter = db.get_chapter_by_id(id)
    if not chapter:
        return abort(404)
    fetched_course = db.get_course_by_id(chapter[1])
    course = {"id": fetched_course[0], "name": fetched_course[1]}
    exercises = db.get_chapter_exercises_and_answers(id)

    return render_template("students/chapters_id.html", id=id, name=chapter[2], content=chapter[3], course=course,
                           exercises=exercises.values())


@app.route("/students/exercises/answer", methods=["POST"])
def students_exercises_answer():
    exercise_id = request.form["exercise_id"]
    answered_id = request.form["answer"]
    correct = db.is_exercise_correct(exercise_id, answered_id)

    if correct:
        return "Right answer!"
    return "Wrong answer!"
