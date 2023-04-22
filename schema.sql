create table users
(
    id       SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);


create table courses
(
    id          SERIAL PRIMARY KEY,
    course_name TEXT,
    description TEXT
);

create table course_teachers
(
    id         SERIAL PRIMARY KEY,
    teacher_id INTEGER REFERENCES users,
    course_id  INTEGER REFERENCES courses
);

create table course_chapters
(
    id              SERIAL PRIMARY KEY,
    course_id       INTEGER REFERENCES courses,
    chapter_name    TEXT,
    chapter_content TEXT
);

create table chapter_exercises
(
    id             SERIAL PRIMARY KEY,
    chapter_id     INTEGER REFERENCES course_chapters,
    question       TEXT,
    correct_answer INTEGER
);


create table exercise_options
(
    id     SERIAL PRIMARY KEY,
    answer TEXT,
    exercise INTEGER REFERENCES chapter_exercises
);
