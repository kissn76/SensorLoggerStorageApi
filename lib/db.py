from datetime import datetime
from lib import db_sqlite as db


def sensordata_insert(sensorid:str, datetime:str, value:float) -> int:
    ret = db.data_insert("sensordata", sensorid=sensorid, datetime=datetime, value=value)
    return ret


def sensordata_validate(sensorid:str, dateAndTime:str, value:float) -> list:
    error_messages = {}
    sensorid_errors = []
    datetime_errors = []
    value_errors = []

    if bool(sensorid) is False:
        sensorid_errors.append("Value is empty")

    if bool(dateAndTime):
        try:
            dateAndTime = datetime.fromisoformat(dateAndTime).strftime("%Y-%m-%d %H:%M:%S")
        except:
            datetime_errors.append(f'Date and time error (valid format: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')
    else:
        datetime_errors.append("Value is empty")

    if bool(value):
        try:
            value = float(str(value).replace(',', '.'))
            if str(value).replace('.', '', 1).isdigit() is False:
                value_errors.append("Value is not a number")
        except ValueError:
            value_errors.append("Value is not a number")
    else:
        value_errors.append("Value is empty")

    if bool(sensorid_errors):
        error_messages.update({"sensorid": sensorid_errors})
    if bool(datetime_errors):
        error_messages.update({"datetime": datetime_errors})
    if bool(value_errors):
        error_messages.update({"value": value_errors})

    return error_messages


def sensordata_select_all() -> list:
    ret = db.data_select("sensordata")
    return ret


def sensordata_select_by_id(id:int) -> list:
    whereClause = f"id={id}"
    ret = db.data_select("sensordata", whereClause=whereClause)
    return ret


def sensordata_select_by_sensorid(sensorid:str) -> list:
    whereClause = f"sensorid='{sensorid}'"
    ret = db.data_select("sensordata", whereClause=whereClause)
    return ret