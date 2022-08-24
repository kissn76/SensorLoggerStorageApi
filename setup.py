from lib import settings
from lib import db_sqlite as db

settings.readSettings()

if __name__ == "__main__":
    db.create_tables()