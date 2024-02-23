import sys
import json

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Not enough arguments")
        exit(1)
    elif len(sys.argv) > 3:
        print("Too many arguments")
    sql_start = "INSERT INTO departments (dept_code, dept_name, school_name) VALUES\n\t"
    sql_mid = ""
    sql_end = ";"
    with open(sys.argv[1], 'r') as json_file:
        json_data = json.load(json_file)
        for school in json_data:
            for dept in school["depts"]:
                sql_mid += "('" + dept["code"] + "', '" + dept["name"] + "', '" + school["name"] + "'),\n\t"
        sql_mid = sql_mid[:-3]
    with open(sys.argv[2], "w") as sql_file:
        sql_file.write(sql_start + sql_mid + sql_end)
