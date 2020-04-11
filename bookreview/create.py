import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://yhzmploiycxzrm:3f46af0b454fafff9c84dd83a380fbe72bc5335bc8a12b5dac2c28dc84ce9e04@ec2-46-137-84-173.eu-west-1.compute.amazonaws.com:5432/de4ufd7h78g7cn"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
