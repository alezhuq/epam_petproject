import os

from dotenv import load_dotenv
from flask import Flask

from models.models import db, migrate
from rest.routes import api

load_dotenv()

HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
NAME = os.getenv("NAME")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")
TEST = os.getenv("TEST")
UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)

app.config["SECRET_KEY"] = "qweasdzxcqwesadxc"

if __name__ == "__main__":
    app.config["SQLALCHEMY_DATABASE_URI"] = f"""{DATABASE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"""

else:
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///:memory:'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

ALLOWED_EXTENTIONS = ('png', 'jpg', 'jpeg',)

db.init_app(app)
migrate.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
