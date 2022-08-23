from flask import Flask, request, jsonify
from datetime import datetime
from lib import db_sqlite as db


app = Flask(__name__)

@app.route('/')
def query_records():
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sensorid:str = request.args.get("sensorid").replace('"', '')
    dateAndTime:str = request.args.get("datetime", default=dt).replace('"', '')
    value:float = float(request.args.get("value", default="0.0").replace('"', ''))
    return jsonify({"sensorid": sensorid, "datetime": dateAndTime, "value": value})

if __name__ == '__main__':
    db.create_tables()
    app.run(debug=True)