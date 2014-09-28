from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from application import config
from sqlalchemy import create_engine


def connect_database():
    engine = create_engine(
        'mysql://' + config.get("HOME", "DATABASE_USER") +
        ':' + config.get("HOME", "DATABASE_PASSWORD") + '@' + config.get("HOME", "DATABASE_HOST")
        + ':' + config.get("HOME", "DATABASE_PORT") + '/' + config.get("HOME", "DATABASE_NAME"),
        echo=False)
    return engine


def generate_database_sub(engine):
    base_in = declarative_base()
    session_in = sessionmaker()
    session_in.configure(bind=engine)
    return base_in, session_in

db = connect_database()

base, session = generate_database_sub(db)

