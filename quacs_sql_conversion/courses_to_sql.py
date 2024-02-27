import sys
import json
import unidecode

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Not enough arguments")
        exit(1)
    elif len(sys.argv) > 3:
        print("Too many arguments")
    sql_start = "INSERT INTO courses (dept, code_num, title, desc_text) VALUES\n\t"
    sql_mid = ""
    sql_end = ";"

    with open(sys.argv[1], 'r') as json_file:
        json_data = json.load(json_file)
        for item in json_data:
            crse = json_data[item]
            description = unidecode.unidecode(crse["description"]).replace("'", "\\'")
            if len(description) == 0:
                description = "NULL"
            else:
                description = "'" + description + "'"
            sql_mid += "('" + unidecode.unidecode(crse["subj"]).replace("'", "\\'") + "', " + unidecode.unidecode(crse["crse"]).replace("'", "\\'") + ", '" + unidecode.unidecode(crse["name"]).replace("'", "\\'") + "', " + description + "),\n\t"
        sql_mid = sql_mid[:-3]
    with open(sys.argv[2], "w",) as sql_file:
        sql_file.write(sql_start + sql_mid + sql_end)
