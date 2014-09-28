from application import config
from sqlalchemy import create_engine
from core.users import Users


def create_db():
    print("Start creation of database")
    engine = create_engine(
        'mysql://' + config.get("HOME", "DATABASE_USER") + ':' + config.get("HOME",
                                                                            "DATABASE_PASSWORD") + '@' + config.get(
            "HOME", "DATABASE_HOST") + ':' + config.get("HOME", "DATABASE_PORT") + '/', echo=False)
    engine.execute("CREATE DATABASE IF NOT EXISTS %s;" % config.get("HOME", "DATABASE_NAME"))
    engine.execute("USE %s" % config.get("HOME", "DATABASE_NAME"))
    Users.metadata.create_all(engine)
    return engine

create_db()