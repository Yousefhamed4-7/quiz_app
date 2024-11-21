from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from flask import Flask
from dotenv import load_dotenv
import os


load_dotenv(os.path.join(Path(__file__).parent,".env"))


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(Path(__file__).parent,'database.db')}"
    app.config["SECRET_KEY"] = os.getenv("secret_key")

    db.init_app(app)

    create_db(app)

    from .utilities import urlprefix,database 
    app.jinja_env.globals.update(geturl=urlprefix.geturl)
    app.jinja_env.globals.update(choices=database.Database.choice_questions_function)


    from .views import view
    from .auths import auth
    from .apis import api
    app.register_blueprint(view,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")
    app.register_blueprint(api,url_prefix="/api")

    return app 


def create_db(app: Flask):
    if not os.path.exists(os.path.join(Path(__file__),"database.db")):
        with app.app_context():
            db.create_all()