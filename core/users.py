import time
import sha3
import uuid
import logging

from sqlalchemy import Column, Integer, String
from core.database import base, session
from application import login_manager

logging.getLogger("Home1.0")


class Users(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    pseudonyme = Column(String(256), default="")
    first_name = Column(String(256), default="")
    last_name = Column(String(256), default="")

    email = Column(String(256), default="")
    __password = Column(String(1024), default="")
    salt = Column(String(128), default="")
    last_login = Column(Integer, default=0)
    status = Column(Integer, default=0)

    def save(self):
        db = session()
        db.add(self)
        db.commit()
        db.close()

    @staticmethod
    def get_by_id(id):
        db = session()
        result = db.query(Users).filter(Users.id == id).one()
        db.close()
        return result

    @staticmethod
    def get_by_pseudonyme(pseudonyme):
        db = session()
        result = db.query(Users).filter(Users.pseudonyme == pseudonyme).one()
        db.close()
        return result

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        salt = ""
        numuuid = len(password) / 32
        while numuuid > 0:
            salt += uuid.uuid4().get_hex()
            numuuid = - 1

        sha = sha3.sha3_512(password + salt)
        password = sha.hexdigest()
        self.salt = salt
        self.__password = password

    @staticmethod
    def authentification(pseudonyme, password):
        try:
            user = Users.get_by_pseudonyme(pseudonyme)
            password = sha3.sha3_512(password + user.salt).hexdigest()
            if password == user.password:
                user.last_login = time.time()
                user.save()
                return True
            else:
                return False
        except Exception as e:
            logging.error(e.message)
            return False

    def is_active(self):
        if self.status >= 1:
            if time.time() - 3600 > self.last_login:
                return False
            else:
                return True
        else:
            return False

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id


