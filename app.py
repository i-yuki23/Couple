import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import apology, login_required, allowed_file, getPastDay

from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'JPG'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///couple.db")

# FOREIGN KEY(user_id) REFERENCES users(id))で二つのtableを繋げる。
db.execute("CREATE TABLE IF NOT EXISTS posts (user_id NUMERIC NOT NULL, image TEXT, \
            text_content TEXT NOT NULL, timestamp TEXT, FOREIGN KEY(user_id) REFERENCES users(id))")

db.execute("CREATE TABLE IF NOT EXISTS pictures (user_id NUMERIC NOT NULL, image TEXT NOT NULL, gender TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))")

db.execute("CREATE TABLE IF NOT EXISTS dates (user_id NUMERIC NOT NULL, date DATETAME NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))")


# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    gender_boy = "boy"
    gender_girl = "girl"


    if request.method == "POST":
        boy = request.files["boy"]
        girl = request.files["girl"]

        if not boy or not girl:
            return apology("Missing image")


        if boy and allowed_file(boy.filename, ALLOWED_EXTENSIONS):
            filename_boy = secure_filename(boy.filename)
            boy.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_boy))
            img_url_boy = filename_boy


        if girl and allowed_file(girl.filename, ALLOWED_EXTENSIONS):
            filename_girl = secure_filename(girl.filename)
            girl.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_girl))
            img_url_girl = filename_girl


            db.execute("INSERT INTO pictures (user_id, image, gender) VALUES (?, ?, ?)", user_id, img_url_boy, gender_boy)
            db.execute("INSERT INTO pictures (user_id, image, gender) VALUES (?, ?, ?)", user_id, img_url_girl, gender_girl)
            return redirect("/")

        else:
            return apology("unavailable files")

    result_boy = db.execute("SELECT image FROM pictures WHERE user_id = ? AND gender = ?", session["user_id"], gender_boy)
    result_girl = db.execute("SELECT image FROM pictures WHERE user_id = ? AND gender = ?", session["user_id"], gender_girl)

    result_date = db.execute("SELECT date FROM dates WHERE user_id = ?", session["user_id"])[0]['date']

    rd = result_date.split('-')

    y = int(rd[0])
    m = int(rd[1])
    d = int(rd[2])

    date = getPastDay(y, m, d)


    return render_template("index.html", result_boy=result_boy, result_girl=result_girl, date=date)


@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    """Buy shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":
        img_file = request.files["img_file"]
        text = request.form.get("text")

        if img_file and allowed_file(img_file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_url = filename

            dt=datetime.now()
            d=dt.date()

            db.execute("INSERT INTO posts (user_id, image, text_content, timestamp) VALUES (?, ?, ?, ?)", user_id, img_url, text, d)

            return render_template("posted.html")

        else:
            return apology("unavailable files")


    else:
        return render_template("post.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/story")
@login_required
def story():

        results = db.execute("SELECT image, text_content, timestamp FROM posts WHERE user_id = ?", session["user_id"])

        return render_template("story.html", results=results)



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        date  = request.form.get("date")

        # Ensure username was submitted
        if username == "":
            return apology("must provide username", 400)

        if len(db.execute("SELECT username FROM users WHERE username = ?", username)) == 1:
            return apology("already exist")

        # Ensure password was submitted
        elif password == "":
            return apology("must provide password", 400)

        elif confirmation != password or confirmation == "":
            return apology("must provide the same password", 400)

        if not date:
            return apology("must provide date")

        # Query database for username
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        db.execute("INSERT INTO dates (user_id, date) VALUES (?, ?)", session["user_id"], date)

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/password", methods=["GET", "POST"])
def password():

    user_id = session["user_id"]

    if request.method == "POST":
        current_password = request.form.get("current_password")
        user_password = db.execute("SELECT hash FROM users WHERE id = ?", user_id)[0]['hash']
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        if not check_password_hash(user_password, current_password):
            return apology("must provide the current password")

        if current_password == "":
            return apology("must provide password", 400)

        if not new_password:
            return apology("must provide new password")

        if confirmation != new_password or confirmation == "":
            return apology("must provide the same password", 400)

        # Query database for username
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new_password), user_id)

        return redirect("/")

    else:
        return render_template("password.html")