CREATE TABLE IF NOT EXISTS courses(
    dept VARCHAR(4) NOT NULL,
    code_num SMALLINT NOT NULL,
    title VARCHAR(255) NOT NULL,
    desc_text TEXT NOT NULL,
    credit_min TINYINT NOT NULL,
    credit_max TINYINT NOT NULL,
    CONSTRAINT pk_courses PRIMARY KEY(dept, code_num)
) COMMENT 'Courses from the RPI catalog';

CREATE TABLE IF NOT EXISTS course_availability(
    dept VARCHAR(4) NOT NULL,
    code_num SMALLINT NOT NULL,
    semester SMALLINT NOT NULL,
    CONSTRAINT pk_course_avail PRIMARY KEY(dept, code_num, semester),
    CONSTRAINT fk_course_avail_courses
        FOREIGN KEY(dept, code_num) REFERENCES courses(dept, code_num)
) COMMENT 'Courses from the RPI catalog';

CREATE TABLE IF NOT EXISTS professors(
    semester SMALLINT NOT NULL,
    dept VARCHAR(4) NOT NULL,
    code_num SMALLINT NOT NULL,
    prof_name VARCHAR(255) NOT NULL,
    CONSTRAINT pk_professors PRIMARY KEY(semester, dept, code_num, prof_name),
    CONSTRAINT fk_professors_courses
        FOREIGN KEY(dept, code_num) REFERENCES courses(dept, code_num)
) COMMENT 'Professors for each course';

CREATE TABLE IF NOT EXISTS seats(
    semester SMALLINT NOT NULL,
    dept VARCHAR(4) NOT NULL,
    code_num SMALLINT NOT NULL,
    seats_filled SMALLINT NOT NULL,
    seats_total SMALLINT NOT NULL,
    CONSTRAINT pk_seats PRIMARY KEY(semester, dept, code_num),
    CONSTRAINT fk_seats_courses
        FOREIGN KEY(dept, code_num) REFERENCES courses(dept, code_num)
) COMMENT 'Seats filled in each course';
