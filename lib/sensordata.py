from datetime import datetime
from lib import settings


if settings.databaseType == "sqlite":
    from lib import db_sqlite as db
elif settings.databaseType == "mysql":
    from lib import db_mysql as db
else:
    from lib import db_sqlite as db

tablename = "sensordata"


class Sensordata:
    def __init__(self, id:int=None, sensorid:str=None, datetime:str=None, value:float=None):
        self.id:int = None
        self.sensorid:str = None
        self.datetime:str = None
        self.value:float = None
        self.error = {}

        if bool(id):
            self.load_by_id(id)
        else:
            self.setClass(sensorid, datetime, value)
            self.id = self.save()


    def validate(self):
        error_messages = {}
        sensorid_errors = []
        datetime_errors = []
        value_errors = []

        if bool(self.sensorid) is False:
            sensorid_errors.append("Value is empty")

        if bool(self.datetime):
            try:
                self.datetime = datetime.fromisoformat(self.datetime).strftime("%Y-%m-%d %H:%M:%S")
            except:
                datetime_errors.append(f'Date and time error (valid format: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')
        else:
            datetime_errors.append("Value is empty")

        if bool(self.value):
            try:
                self.value = float(str(self.value).replace(',', '.'))
                if str(self.value).replace('.', '', 1).isdigit() is False:
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

        self.error = error_messages


    def save(self) -> int:
        ret = None
        self.validate()
        if self.id is None and len(self.error) == 0:
            ret = db.data_insert(tablename, sensorid=self.sensorid, datetime=self.datetime, value=self.value)
        else:
            pass # update
        return ret


    def load_by_id(self, id):
        whereClause = f"id={id}"
        p = db.data_select(tablename, whereClause=whereClause)
        if bool(p):
            p = p[0]
            id, sensorid, datetime, value = p
            self.id = id
            self.setClass(sensorid, datetime, value)


    def setClass(self, sensorid:str, datetime:str, value:float):
        self.sensorid = sensorid
        self.datetime = datetime
        self.value = value


    def getId(self) -> int:
        return self.id


    def getSensorid(self) -> str:
        return self.sensorid


    def getDatetime(self) -> str:
        return self.datetime


    def getValue(self) -> float:
        return float(self.value)


    def getError(self) -> list:
        return self.error


    def __repr__(self):
        return f"{self.id} {self.sensorid} {self.datetime} {self.value}"


    def getAsDictionary(self) -> dict:
        return {"id": self.id, "sensorid": self.sensorid, "datetime": self.datetime, "value": self.value}


    def print(self):
        print(self.__repr__())


def getAll() -> list:
    objects = {}
    elements = db.data_select(tablename)
    for element in elements:
        id = element[0]
        obj = Sensordata(id)
        objects.update({obj.getId(): obj})
    return objects


def getAllBySensorId(sensorId:str) -> list:
    objects = {}
    whereClause = f"sensorid='{sensorId}'"
    elements = db.data_select(tablename, whereClause=whereClause)
    for element in elements:
        id = element[0]
        obj = Sensordata(id)
        objects.update({obj.getId(): obj})
    return objects


def printAll() -> list:
    objects = getAll()
    for objId in objects:
        objects[objId].print()