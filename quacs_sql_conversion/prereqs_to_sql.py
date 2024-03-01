import sys
import os
import json

def prereq(values):
    return

def coreq(values):
    return

def restriction(values):
    return

def cross_list(values):
    return

def oops(value):
    print("key: ", value)

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
    sql_start = "UPDATE sections SET prereq_desc = "
    sql_mid = ""
    sql_where = " WHERE crn = "
    sql_end = ";\n"

    with open(file_to_read, 'r') as f:
        json_data = json.load(f)
        for crn in json_data:
            section = json_data[crn]
            for key in section:
                if key == 'prerequisites':
                    prereq(True)
                elif key == 'corequisites':
                    coreq(True)
                elif key == 'restrictions':
                    prereq(True)
                elif key == 'cross_list_courses':
                    cross_list(True)
                else:
                    oops(key)
            if 'prerequisites' in section:
                pass
                # sql_mid = "'" + str(section['prerequisites']) + "'"
                # final_sql += sql_start + sql_mid + sql_where + sql_end
    with open(os.path.dirname(os.path.abspath(__file__)) + "/data_insertion_sql/prereq_insert.sql", "w",) as sql_file:
        sql_file.write(final_sql)