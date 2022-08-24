# pip install Flask
# pip install Flask-HTTPAuth
# pip install pyopenssl
import configparser
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from lib import sensordata


app = Flask(__name__)
auth = HTTPBasicAuth()

config = configparser.ConfigParser()
config.read("passwd")
users = {}
for confSectionName in config.sections():
    for key, val in config.items(confSectionName):
        users.update({key: generate_password_hash(val)})


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@app.route('/', methods=['GET'])
@auth.login_required
def query_records_get():
    sensorid:str = None
    dateAndTime:str = None
    value:float = None

    try:
        sensorid = request.args.get("sensorid").replace('"', '').replace("'", "")
    except:
        pass
    try:
        dateAndTime = request.args.get("datetime").replace('"', '').replace("'", "")
    except:
        pass
    try:
        value = request.args.get("value").replace('"', '').replace("'", "").replace(",", ".")
    except:
        pass

    ret = saveData(sensorid, dateAndTime, value)
    return ret


@app.route('/', methods=['POST'])
@auth.login_required
def query_records_post():
    content = request.json
    sensorid:str = None
    dateAndTime:str = None
    value:float = None

    try:
        sensorid = content["sensorid"].replace('"', '').replace("'", "")
    except:
        pass
    try:
        dateAndTime = content["datetime"].replace('"', '').replace("'", "")
    except:
        pass
    try:
        value = str(content["value"]).replace('"', '').replace("'", "").replace(",", ".")
    except:
        pass

    ret = saveData(sensorid, dateAndTime, value)
    return ret


def saveData(sensorid:str, dateAndTime:str, value:float) -> list:
    sd = sensordata.Sensordata(None, sensorid, dateAndTime, value)
    ret = []
    if bool(sd.getError()):
        ret = sd.getError()
    else:
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datas = sensordata.getBySensorId(sensorid)
        for d in datas:
            d = sensordata.Sensordata(d)
            ret.append(d.getAsDictionary())

    return ret


if __name__ == "__main__":
    app.run(ssl_context="adhoc", debug=True)