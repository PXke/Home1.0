import ConfigParser
import logging

from flask import Flask
from flask_login import LoginManager

from core.views import core_pages
from core.utils import generate_secret_key
app = Flask(__name__)
app.register_blueprint(core_pages)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"

logging.getLogger("Home1.0")

config = ConfigParser.ConfigParser()
config_file = open('configuration.conf')
config.readfp(config_file)
config_file.close()
keys_to_check = ["DATABASE_HOST", "DATABASE_PASSWORD", "DATABASE_NAME", "DATABASE_PORT",
                 "DATABASE_USER", "SECRET_KEY"]

if __name__ == "__main__":

    print("Home1.0 Ignition Started")
    print("configuration checking")
    for key in keys_to_check:
        try:
            config.get("HOME", key)
            print("{0}...{1}Ok".format(key, (80 - 5 - len(key)) * " "))
        except ConfigParser.NoOptionError:
            print("Please give a value to {0}.".format(key))
            if not key in ["SECRET_KEY"]:
                user_input = raw_input()
                config.set("HOME", key, user_input)
            else:
                action = {"SECRET_KEY": generate_secret_key }
                result = action[key]()
                config.set("HOME", key, result)

    config_file = open('configuration.conf', "w")
    config.write(config_file)
    config_file.close()

    from core.database import db, session
    from sqlalchemy.exc import OperationalError
    from sqlalchemy.orm.exc import NoResultFound
    try:
        db.table_names()
    except OperationalError:
        from createdb import create_db
        create_db()

    db.table_names()

    from core.users import Users
    try:
        session().query(Users).filter(Users.pseudonyme == "Admin").one()
    except NoResultFound:
        print("Admin new password ?:")
        user_input = raw_input()
        admin_user = Users()
        admin_user.pseudonyme = "Admin"
        admin_user.password = user_input
        admin_user.save()
    app.secret_key = config.get("HOME", "SECRET_KEY")
    app.run(host='0.0.0.0', debug=True, use_reloader=True)

