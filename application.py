import ConfigParser

from flask import Flask
from flask_login import LoginManager

from core.views import core_pages

app = Flask(__name__)
app.register_blueprint(core_pages)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"

config = ConfigParser.ConfigParser()
config_file = open('configuration.conf')
config.readfp(config_file)
config_file.close()
keys_to_check = ["DATABASE_HOST", "DATABASE_PASSWORD", "DATABASE_NAME", "DATABASE_PORT",
                 "DATABASE_USER"]

if __name__ == "__main__":

    print("Home1.0 Ignition Started")
    print("configuration checking")
    for key in keys_to_check:
        try:
            config.get("HOME", key)
            print("{0}...{1}Ok".format(key, (80 - 5 - len(key)) * " "))
        except ConfigParser.NoOptionError:
            print("Please give a value to {0}.".format(key))
            user_input = raw_input()
            config.set("HOME", key, user_input)

    config_file = open('configuration.conf', "w")
    config.write(config_file)
    config_file.close()

    from core.database import db, session
    from sqlalchemy.exc import OperationalError
    try:
        db.table_names()
    except OperationalError:
        from createdb import create_db
        create_db()

    db.table_names()
    from core.users import Users
    if not session.query(Users).filter(Users.pseudonyme == "Admin").one():
        admin_user = Users()
        admin_user.pseudonyme = "Admin"
        admin_user.password = setPassword()
    app.run("127.0.0.1")
