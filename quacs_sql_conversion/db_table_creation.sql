CREATE TABLE departments(
    dept_code VARCHAR(255) NOT NULL,
    dept_name VARCHAR(255) NOT NULL,
    school_name VARCHAR(255) NOT NULL,
    CONSTRAINT pk_departments PRIMARY KEY(dept_code)
) COMMENT 'Data about departments and corresponding schools';

CREATE TABLE courses(  
    dept VARCHAR(255) NOT NULL,
    code_num INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    desc_text TEXT,
    CONSTRAINT pk_courses PRIMARY KEY(dept, code_num)
) COMMENT 'Data for all courses';

CREATE TABLE sections(
    crn INT NOT NULL,
    dept VARCHAR(255) NOT NULL,
    code_num INT NOT NULL,
    sec_num INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    seat_max INT NOT NULL,
    credit_min INT NOT NULL,
    credit_max INT NOT NULL,
    prereq_desc TEXT,
    CONSTRAINT pk_sections PRIMARY KEY(crn),
    CONSTRAINT fk_sections_courses FOREIGN KEY(dept, code_num) REFERENCES courses(dept, code_num)
) COMMENT 'Section data for each course';

CREATE TABLE timeslots(
    crn INT NOT NULL,
    time_id INT NOT NULL,
    instructor VARCHAR(255) NOT NULL,
    room VARCHAR(255) NOT NULL,
    date_start DATE NOT NULL,
    date_end DATE NOT NULL,
    days_week VARCHAR(255) NOT NULL,
    time_start TIME NOT NULL,
    time_end TIME NOT NULL,
    CONSTRAINT pk_timeslots PRIMARY KEY(crn, time_id),
    CONSTRAINT fk_timeslots_sections FOREIGN KEY(crn) REFERENCES sections(crn)
) COMMENT 'Timeslot data for each section';