import sqlite3
from sqlite3 import Error
from datetime import datetime


def create_connection(db_file:str="database.db") -> sqlite3.Connection:
    conn = None
    base_path = "./data/"
    path = base_path + db_file

    try:
        conn = sqlite3.connect(path)
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
    sql_create_table_sensordata = """ CREATE TABLE IF NOT EXISTS sensordata (
                                        id integer PRIMARY KEY,
                                        sensorid text NOT NULL,
                                        datetime text NOT NULL,
                                        value real NOT NULL
                                    ); """

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


def sensordata_insert(sensorid:str, datetime:str, value:float) -> int:
    ret = data_insert("sensordata", sensorid=sensorid, datetime=datetime, value=value)
    return ret


def sensordata_validate(sensorid:str, dateAndTime:str, value:float) -> list:
    error_messages = {}
    sensorid_errors = []
    datetime_errors = []
    value_errors = []

    if bool(sensorid) is False:
        sensorid_errors.append("Value is empty")

    if bool(dateAndTime) is False:
        datetime_errors.append("Value is empty")
    try:
        dateAndTime = datetime.fromisoformat(dateAndTime).strftime("%Y-%m-%d %H:%M:%S")
    except:
        datetime_errors.append(f'Date and time error (format: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')

    value = float(str(value).replace(',', '.'))
    if str(value).replace('.', '', 1).isdigit() is False:
        value_errors.append("Value is not a number")

    if bool(sensorid_errors):
        error_messages.update({"sensorid": sensorid_errors})
    if bool(datetime_errors):
        error_messages.update({"datetime": datetime_errors})
    if bool(value_errors):
        error_messages.update({"value": value_errors})

    return error_messages


def sensordata_select_all() -> list:
    ret = data_select("sensordata")
    return ret


def sensordata_select_by_id(id:int) -> list:
    whereClause = f"id={id}"
    ret = data_select("sensordata", whereClause=whereClause)
    return ret


def sensordata_select_by_sensorid(sensorid:str) -> list:
    whereClause = f"sensorid='{sensorid}'"
    ret = data_select("sensordata", whereClause=whereClause)
    return ret