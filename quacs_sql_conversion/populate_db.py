import pymysql
from pymysql.constants import CLIENT
import sqlparse

db_host = ""
db_port = 0
db_user = ""
db_pass = ""
db_schema = "bot_data"
db_conn = None
db_cursor = None

def run_query(sql_file):
    with open(sql_file, "r") as f:
        content = f.read()
    
    queries = sqlparse.split(content)
    queries = [query.strip() for query in queries if query.strip()]

    for query in queries:
        db_cursor.execute(query)
    db_conn.commit()

    print(f"Query {sql_file} executed")

    db_cursor.fetchall()

def database_connect():
    conn = pymysql.connect(user=db_user, password=db_pass, host=db_host, port=db_port, client_flag=CLIENT.MULTI_STATEMENTS)
    print("Database connection established")
    cursor = conn.cursor()
    return conn, cursor

def db_conn_cleanup():
    db_cursor.close()
    db_conn.close()
    print("Database connection and cursor closed")

if __name__ == "__main__":
    sql_files = [
        "db_table_creation.sql",
        "data_insertion_sql/dept_insert.sql",
        "data_insertion_sql/crse_insert.sql",
        "data_insertion_sql/sctn_insert.sql",
        "data_insertion_sql/prereq_insert.sql",
        "data_insertion_sql/tmslt_insert.sql",
        "data_insertion_sql/tmslt_days_insert.sql",
        "data_insertion_sql/tmslt_profs_insert.sql"
    ]
    
    db_conn, db_cursor = database_connect()

    for file in sql_files:
        run_query(file)

    db_conn_cleanup()
