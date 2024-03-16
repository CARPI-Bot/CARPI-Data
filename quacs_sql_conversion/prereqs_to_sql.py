import sys
import os
import json

def prereq(values):
    if len(values) == 0:
        raise ValueError("No values in prerequisites dictionary")
    if "nested" in values:
        return "'" + nested(values['nested'], values['type']) + "'"
    desc_str = ""
    for key in values:
        if key == "course":
            desc_str += values[key] + ", "
        elif key == "type":
            pass
        else:
            oops("prereq", key)
    return "'" + desc_str[:-2] + "'"

def nested(values, nest_type):
    if len(values) == 0:
        raise ValueError("Nothing in nested array")
    nested_string = ""
    for arr in values:
        for key in arr:
            if key == "course":
                nested_string += arr[key] + " " + nest_type + " "
            elif key == "nested":
                nested_string += "(" + nested(arr['nested'], arr['type']) + ") " + nest_type + " "
            elif key == "type":
                pass
            else:
                oops("nested", key)
    return nested_string[:-(2 + len(nest_type))]

def coreq(values):
    if len(values) == 0:
        raise ValueError("No values in corequisites array")
    final_string = ""
    for course in values:
        final_string += course[:course.index("-")] + " " + course[course.index("-") + 1:] + ", "
    return "'" + final_string[:-2] + "'"

def restriction(values):
    if len(values) == 0:
        raise ValueError("No values in restriction dictionary")
    desc_str = ""
    for key in values:
        if key == "level":
            desc_str += "Level: " + could_be(values[key], key) + "; "
        elif key == "major":
            desc_str += "Major: " + could_be(values[key], key) + "; "
        elif key == "classification":
            desc_str += "Classification: " + could_be(values[key], key) + "; "
        elif key == "degree":
            desc_str += "Degree: " + could_be(values[key], key) + "; "
        elif key == "field_of_study":
            desc_str += "Field of Study: " + could_be(values[key], key) + "; "
        elif key == "campus":
            desc_str += "Campus: " + could_be(values[key], key) + "; "
        elif key == "college":
            desc_str += "College: " + could_be(values[key], key) + "; "
        else:
            oops("restriction", key)
    return "'" + desc_str[:-2] + "'"

def could_be(values, origin):
    if len(values) == 0:
        raise ValueError(f"No values in {origin} dictionary")
    desc_str = ""
    for key in values:
        if key == "must_be":
            desc_str += "Must be "
            for val in values[key]:
                desc_str += val + " or "
        elif key == "may_not_be":
            desc_str += "May not be "
            for val in values[key]:
                desc_str += val + " or "
        else:
            oops("could_be", key)
    return desc_str[:-4]

def cross_list(values):
    if len(values) == 0:
        raise ValueError("No values in cross_list_courses array")
    final_string = ""
    for course in values:
        final_string += course[:course.index("-")] + " " + course[course.index("-") + 1:] + ", "
    return "'" + final_string[:-2] + "'"


def oops(source, value):
    raise ValueError(f"Dictionary key \"{value}\" not accounted for in {source}() function")

if __name__ == '__main__':
    file_to_read = ""
    if len(sys.argv) < 2:
        file_to_read = input("Path to JSON file: ")
    elif len(sys.argv) > 2:
        print("Too many arguments")
        exit(0)
    else:
        file_to_read = sys.argv[1]
    final_sql = ""

    with open(file_to_read, 'r') as f:
        json_data = json.load(f)
        for crn in json_data:
            section = json_data[crn]
            prq = "NULL"
            crq = "NULL"
            rst = "NULL"
            csl = "NULL"
            for key in section:
                match key:
                    case 'prerequisites':
                        prq = prereq(section[key])
                    case 'corequisites':
                        crq = coreq(section[key])
                    case 'restrictions':
                        rst = restriction(section[key])
                    case 'cross_list_courses':
                        csl = cross_list(section[key])
                    case _:
                        oops("main", key)
            final_sql += f"UPDATE sections SET prereq_desc = {prq}, coreq_desc = {crq}, restrict_desc = {rst}, cross_list_desc = {csl} WHERE crn = {crn};\n"
    with open(os.path.dirname(os.path.abspath(__file__)) + "/data_insertion_sql/prereq_insert.sql", "w",) as sql_file:
        sql_file.write(final_sql)