-- drop existing tables to be replaced
DROP TABLE IF EXISTS seats;
DROP TABLE IF EXISTS professors;
DROP TABLE IF EXISTS course_relationships;
DROP TABLE IF EXISTS course_availability;
DROP TABLE IF EXISTS courses;

-- create the tables
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
    sem_year SMALLINT NOT NULL,
    semester ENUM('Fall', 'Spring', 'Summer') NOT NULL,
    CONSTRAINT pk_course_avail PRIMARY KEY(dept, code_num, sem_year, semester),
    CONSTRAINT fk_course_avail_courses
        FOREIGN KEY(dept, code_num) REFERENCES courses(dept, code_num)
) COMMENT 'Courses from the RPI catalog';

CREATE TABLE IF NOT EXISTS course_relationships(
    dept VARCHAR(4) NOT NULL,
    code_num SMALLINT NOT NULL,
    relationship ENUM('Coreq', 'Cross') NOT NULL,
    rel_dept VARCHAR(4) NOT NULL,
    rel_code_num SMALLINT NOT NULL,
    CONSTRAINT pk_course_rels
        PRIMARY KEY(dept, code_num, relationship, rel_dept, rel_code_num),
    CONSTRAINT fk_course_rels_courses
        FOREIGN KEY(dept, code_num) REFERENCES courses(dept, code_num)
) COMMENT 'Courses that are corequisites or crosslists for other courses';

CREATE TABLE IF NOT EXISTS professors(
    sem_year SMALLINT NOT NULL,
    semester ENUM('Fall', 'Spring', 'Summer') NOT NULL,
    dept VARCHAR(4) NOT NULL,
    code_num SMALLINT NOT NULL,
    prof_name VARCHAR(255) NOT NULL,
    CONSTRAINT pk_professors PRIMARY KEY(sem_year, semester, dept, code_num, prof_name),
    CONSTRAINT fk_professors_courses
        FOREIGN KEY(dept, code_num) REFERENCES courses(dept, code_num)
) COMMENT 'Professors for each course';

CREATE TABLE IF NOT EXISTS seats(
    sem_year SMALLINT NOT NULL,
    semester ENUM('Fall', 'Spring', 'Summer') NOT NULL,
    dept VARCHAR(4) NOT NULL,
    code_num SMALLINT NOT NULL,
    seats_filled SMALLINT NOT NULL,
    seats_total SMALLINT NOT NULL,
    CONSTRAINT pk_seats PRIMARY KEY(sem_year, semester, dept, code_num),
    CONSTRAINT fk_seats_courses
        FOREIGN KEY(dept, code_num) REFERENCES courses(dept, code_num)
) COMMENT 'Seats filled in each course';