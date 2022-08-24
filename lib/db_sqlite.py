import sqlite3
from sqlite3 import Error
from lib import settings


sqlitePath = None
if bool(settings.sqlitePath):
    sqlitePath = settings.sqlitePath
else:
    sqlitePath = "./data/database.db"


def create_connection() -> sqlite3.Connection:
    conn = None
    try:
        conn = sqlite3.connect(sqlitePath)
    except Error as e:
        print(e)

    return conn


def create_table(create_table_sql:str):
    conn = create_connection()
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute(create_table_sql)
        except Error as e:
            print(e)
    else:
        print("Error! Cannot create the database connection.")
    conn.close()


def create_tables():
    sql_create_table_sensordata = """CREATE TABLE IF NOT EXISTS sensordata (
                                        id integer PRIMARY KEY,
                                        sensorid text NOT NULL,
                                        datetime text NOT NULL,
                                        value real NOT NULL
                                    );"""

    create_table(sql_create_table_sensordata)


def data_insert(table:str, **values) -> int:
    columnNames = ', '.join(values.keys())
    columnValues = ', '.join(['?'] * len(values))
    sql = f"INSERT INTO {table} ({columnNames}) VALUES ({columnValues})"
    ret = None

    conn = create_connection()
    if bool(conn):
        try:
            cur = conn.cursor()
            cur.execute(sql, tuple(values.values()))
            conn.commit()
            ret = cur.lastrowid
        except Error as e:
            print(e)
    else:
        print("Error! Cannot create the database connection.")
    conn.close()

    return ret


def data_select(table:str, fields:tuple=("*",), whereClause:str=None) -> list:
    ret = None

    selectFields = ','.join(fields)
    sql = f"SELECT {selectFields} FROM {table}"

    if bool(whereClause):
        sql += f" WHERE {whereClause}"

    conn = create_connection()
    if bool(conn):
        try:
            cur = conn.cursor()
            cur.execute(sql)
            ret = cur.fetchall()
        except Error as e:
            print(e)
    else:
        print("Error! Cannot create the database connection.")
    conn.close()

    return ret