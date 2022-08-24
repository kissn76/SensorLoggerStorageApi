import configparser

settingsFile = "settings.ini"

users = {}
databaseType = None
sqlitePath = None
mysqlHost = None
mysqlUser = None
mysqlPasswd = None
mysqlDatabase = None

def readSettings():
    config = configparser.ConfigParser()
    config.read(settingsFile)
    for key, val in config.items("USERS"):
        users.update({key: val})

    databaseType = config["DATABASE"]["type"]
    sqlitePath = config["SQLITE"]["path"]
    mysqlHost = config["MYSQL"]["host"]
    mysqlUser = config["MYSQL"]["user"]
    mysqlPasswd = config["MYSQL"]["passwd"]
    mysqlDatabase = config["MYSQL"]["database"]