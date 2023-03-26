create table users
(
    id       SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);


create table course
(
    id          SERIAL PRIMARY KEY,
    course_name TEXT
);