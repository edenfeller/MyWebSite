from flask import Flask, render_template, jsonify, request, session
from models import *
from sqlalchemy import or_
from flask_session import Session


app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://yhzmploiycxzrm:3f46af0b454fafff9c84dd83a380fbe72bc5335bc8a12b5dac2c28dc84ce9e04@ec2-46-137-84-173.eu-west-1.compute.amazonaws.com:5432/de4ufd7h78g7cn"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.config["SECRET_KEY"] = "HakomonA"

@app.route("/")
def index():
    if session.get("user_id") is None:
       return  render_template("login.html")
    book = Book.query.all()
    return render_template("index2.html", books=books)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method=="GET":
        return  render_template("login.html")
    userPass = request.form.get("password")
    userName = request.form.get("username")
    exist = User.query.filter_by(username = userName).first()
    if not exist:
        return  render_template("login.html", msg="user does not exist. if you dont have an account register")
    if exist.password == userPass:
        session["user_id"] = exist.id
        return index()
    else:
        return  render_template("login.html", msg="wrong password")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method=="GET":
        return  render_template("register.html")
    userPass = request.form.get("password")
    userName = request.form.get("username")
    exist = User.query.filter_by(username = userName).first()
    if not exist:
        newuser = User(username = userName, password = userPass)
        db.session.add(newuser)
        db.session.commit()
        exist = User.query.filter_by(username = userName).first()
        if exist:
            session["user_id"] = exist.id
            return index()


@app.route("/books")
def books():
    """List all books."""
    books = Book.query.all()
    return render_template("books.html", books_list=books)


@app.route("/books/<string:isbn>", methods=["GET","POST"])
def book(isbn):
    """List details about a single book."""

    # Make sure book exists.
    book = Book.query.get(isbn)
    if book is None:
        return render_template("error.html", message="No such book.")
    return render_template("book.html", book=book)


@app.route("/post_review", methods=["POST"])
def post_review(ISBN):
    book = Book.query.get(isbn)
    review = request.form.get("review")
    book.add_review(review=review, book_isbn=isbn, user_id=session["user_id"])
    return book(isbn)


@app.route("/search", methods=["GET","POST"])
def search():
    '''
      if session.get("user_id") is None:
           return  render_template("homepage.html")
    '''
    if request.method=="GET":
        return  render_template("search.html", content="")
    else:
        formcontent = request.form.get("content").lower()
        results= Book.query.filter(or_(Book.isbn.like(f"%{formcontent}%"),Book.title.like(f"%{formcontent}%"),Book.author.like(f"%{formcontent}%"),Book.year.like(f"%{formcontent}%"))).limit(10).all()
        return  render_template("search.html",results=results, content=f'Results for "{formcontent}":')