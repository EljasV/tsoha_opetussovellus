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