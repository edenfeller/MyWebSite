import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://yhzmploiycxzrm:3f46af0b454fafff9c84dd83a380fbe72bc5335bc8a12b5dac2c28dc84ce9e04@ec2-46-137-84-173.eu-west-1.compute.amazonaws.com:5432/de4ufd7h78g7cn"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        book = Book(isbn=isbn.lower(), title=title.lower(), author=author.lower(), year=year)
        db.session.add(book)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
