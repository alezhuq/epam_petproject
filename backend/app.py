import os

from dotenv import load_dotenv
from flask import Flask

from backend.models.models import db, migrate
from backend.rest.routes import api

load_dotenv()

HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
NAME = os.getenv("NAME")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")
TEST = True
UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
ALLOWED_EXTENTIONS = ('png', 'jpg', 'jpeg',)
app.config["SECRET_KEY"] = "qweasdzxcqwesadxc"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16*1024*1024
if TEST is True:
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///:memory:'
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"""{DATABASE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"""

    db.init_app(app)
    migrate.init_app(app)

    with app.app_context():
        db.create_all()

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)


