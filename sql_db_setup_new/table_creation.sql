-- drop existing tables to be replaced
DROP TABLE IF EXISTS seats;
DROP TABLE IF EXISTS professors;
DROP TABLE IF EXISTS course_restrictions;
DROP TABLE IF EXISTS prereq_courses;
DROP TABLE IF EXISTS prereq_structure;
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
    CONSTRAINT pk_courses
        PRIMARY KEY(dept, code_num)
) COMMENT 'Courses from the RPI catalog';

CREATE TABLE IF NOT EXISTS course_availability(
    dept VARCHAR(4) NOT NULL,
    code_num SMALLINT NOT NULL,
    sem_year SMALLINT NOT NULL,
    semester ENUM('Fall', 'Spring', 'Summer') NOT NULL,
    CONSTRAINT pk_course_avail
        PRIMARY KEY(dept, code_num, sem_year, semester),
    CONSTRAINT fk_course_avail_courses
        FOREIGN KEY(dept, code_num)
        REFERENCES courses(dept, code_num)
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
        FOREIGN KEY(dept, code_num)
        REFERENCES courses(dept, code_num)
) COMMENT 'Courses that are corequisites or crosslists for other courses';

CREATE TABLE IF NOT EXISTS prereq_structure(
    dept VARCHAR(4) NOT NULL,
    code_num SMALLINT NOT NULL,
    nesting_id TINYINT NOT NULL,
    relationship ENUM('AND', 'OR'),
    parent_id TINYINT,
    CONSTRAINT pk_prereq_structure
        PRIMARY KEY(dept, code_num, nesting_id),
    CONSTRAINT fk_prereq_structure_courses
        FOREIGN KEY(dept, code_num)
        REFERENCES courses(dept, code_num),
    CONSTRAINT fk_prereq_structure_parent
        FOREIGN KEY(dept, code_num, parent_id)
        REFERENCES prereq_structure(dept, code_num, nesting_id)
) COMMENT 'The structure of prerequisite nesting for each course';


CREATE TABLE IF NOT EXISTS prereq_courses(
    dept VARCHAR(4) NOT NULL,
    code_num SMALLINT NOT NULL,
    parent_id TINYINT NOT NULL,
    req_dept VARCHAR(4) NOT NULL,
    req_code_num SMALLINT NOT NULL,
    CONSTRAINT pk_prereq_courses
        PRIMARY KEY(dept, code_num, parent_id, req_dept, req_code_num),
    CONSTRAINT fk_prereq_courses_courses
        FOREIGN KEY(dept, code_num)
        REFERENCES courses(dept, code_num),
    CONSTRAINT fk_prereq_courses_structure
        FOREIGN KEY(dept, code_num, parent_id)
        REFERENCES prereq_structure(dept, code_num, nesting_id)
) COMMENT 'Prerequisites for other courses, nested according to prereq_structure';

CREATE TABLE IF NOT EXISTS course_restrictions(
    dept VARCHAR(4) NOT NULL,
    code_num SMALLINT NOT NULL,
    category ENUM(
        'Level',
        'Major',
        'Classification',
        'Degree',
        'Field',
        'Campus',
        'College'
    ) NOT NULL,
    restr_rule ENUM('Must be', 'May not be') NOT NULL,
    restriction VARCHAR(255) NOT NULL,
    CONSTRAINT pk_course_restrictions
        PRIMARY KEY(dept, code_num, category, restr_rule, restriction),
    CONSTRAINT fk_course_restrictions_courses
        FOREIGN KEY(dept, code_num)
        REFERENCES courses(dept, code_num)
) COMMENT 'Restrictions for each course';

CREATE TABLE IF NOT EXISTS professors(
    sem_year SMALLINT NOT NULL,
    semester ENUM('Fall', 'Spring', 'Summer') NOT NULL,
    dept VARCHAR(4) NOT NULL,
    code_num SMALLINT NOT NULL,
    prof_name VARCHAR(255) NOT NULL,
    CONSTRAINT pk_professors
        PRIMARY KEY(sem_year, semester, dept, code_num, prof_name),
    CONSTRAINT fk_professors_courses
        FOREIGN KEY(dept, code_num)
        REFERENCES courses(dept, code_num)
) COMMENT 'Professors for each course';

CREATE TABLE IF NOT EXISTS seats(
    sem_year SMALLINT NOT NULL,
    semester ENUM('Fall', 'Spring', 'Summer') NOT NULL,
    dept VARCHAR(4) NOT NULL,
    code_num SMALLINT NOT NULL,
    seats_filled SMALLINT NOT NULL,
    seats_total SMALLINT NOT NULL,
    CONSTRAINT pk_seats
        PRIMARY KEY(sem_year, semester, dept, code_num),
    CONSTRAINT fk_seats_courses
        FOREIGN KEY(dept, code_num)
        REFERENCES courses(dept, code_num)
) COMMENT 'Seats filled per semester for each course';
