from lib import db


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
        valid = db.sensordata_validate(self.sensorid, self.datetime, self.value)
        self.error = valid


    def save(self) -> int:
        ret = None
        self.validate()
        if self.id is None and len(self.error) == 0:
            ret = db.sensordata_insert(self.sensorid, self.datetime, self.value)
        else:
            pass # update
        return ret


    def load_by_id(self, id):
        p = db.sensordata_select_by_id(id)
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


    def getAsString(self):
        return f"{self.id} {self.sensorid} {self.datetime} {self.value}"


    def getAsDictionary(self) -> dict:
        return {"id": self.id, "sensorid": self.sensorid, "datetime": self.datetime, "value": self.value}


    def print(self):
        print(self.getAsString())


def getAll() -> list:
    objects = {}
    elements = db.sensordata_select_all()
    for element in elements:
        id = element[0]
        obj = Sensordata(id)
        objects.update({obj.getId(): obj})
    return objects


def getBySensorId(sensorId:str) -> list:
    objects = {}
    elements = db.sensordata_select_by_sensorid(sensorId)
    for element in elements:
        id = element[0]
        obj = Sensordata(id)
        objects.update({obj.getId(): obj})
    return objects


def printAll() -> list:
    objects = getAll()
    for objId in objects:
        objects[objId].print()