from flask import Flask, render_template, request, g, url_for, session, redirect
import sqlite3
import re


app = Flask(__name__)
app.secret_key = "test"

database = sqlite3.connect("data/database.db")
DATABASE = "data/database.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def is_logged():
    return session.get("loggedin", None)


def user_data():
    user = {"username": session["username"]}
    print(session["username"])
    database = get_db()
    cursor = database.cursor()
    user_data = cursor.execute("SELECT pp,level FROM users WHERE username = ?", (session["username"],)).fetchall()[0]
    user["pp"] = user_data[0]
    user["level"] = {"bar":7,"lvl":user_data[1]}
    return user

@app.route("/")
def index():
	if is_logged():
		return render_template("index.html", connected=True)
	return render_template("index.html", connected=False)



@app.route("/prejuge")
def prejuge():
	if is_logged():
		return render_template("info_folder/prejuge.html", connected=True)
	return render_template("info_folder/prejuge.html", connected=False)

@app.route("/info")
def info():
	if is_logged():
		return render_template("info_folder/info.html", connected=True)
	return render_template("info_folder/info.html", connected=False)
	


@app.route("/contraception")
def contraception():
	if is_logged():
		return render_template("info_folder/contraception.html", connected=True)
	return render_template("info_folder/contraception.html", connected=False)


@app.route("/ist")
def ist():
	if is_logged():
		return render_template("info_folder/ist.html", connected=True)
	return render_template("info_folder/ist.html", connected=False)


@app.route("/sis")
def sis():
	if is_logged():
		return render_template("info_folder/presentation_sis.html", connected=True)
	return render_template("info_folder/presentation_sis.html", connected=False)


@app.route("/games/cartes/")
def cartes():
	if is_logged():
		return render_template("games_folder/cartes.html", connected=True)
	return render_template("games_folder/cartes.html", connected=False)

@app.route("/profil/")
def profil():
    if is_logged():
        user = user_data()
        
        return render_template("user/profil.html", user=user)
    
    return redirect(url_for("login"))

@app.route("/quizz/")
def quizz():
    return render_template("games_folder/quizz.html")

@app.route("/pendu")
def pendu():
	if is_logged():
		return render_template("games_folder/pendu.html", connected=True)
	return render_template("games_folder/pendu.html", connected=False)



@app.route("/register/", methods=["GET", "POST"])
def register():
    # Output message if something goes wrong...
    msg = ""
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        # Create variables for easy access
        username = request.form["username"]
        password = request.form["password"]
        user_age = request.form["age"]
        try:
            if user_age != "":
                user_age = int(user_age)
                if user_age < 13:
                    user_age = "Sorry, you are too young :("
        except ValueError:
            user_age = "Age must be an Integer"

        # Check if account exists
        database = get_db()
        cursor = database.cursor()

        account = cursor.execute(
            "SELECT username FROM users WHERE username = ?", (username,)
        ).fetchone()

        # If account exists show error and validation checks
        if account:
            msg = "Account already exists!"
        elif not re.match(r"[A-Za-z0-9]+", username):
            msg = "Username must contain only characters and numbers!"
        elif not username or not password or not user_age:
            msg = "Please fill out the form!"
        elif isinstance(user_age, str):
            msg = user_age
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute(
                "INSERT INTO users VALUES (?, ?, ?, ?, ?)",
                (username, password, "", 0, user_age),
            )
            database.commit()
            msg = "You have successfully registered!"
            return redirect(url_for("login"))

    return render_template("registration/register.html", msg=msg)


@app.route("/login/", methods=["GET", "POST"])
def login():
    # Output message if something goes wrong...
    msg = ""
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        # Create variables for easy access
        username = request.form["username"]
        password = request.form["password"]

        database = get_db()
        cursor = database.cursor()
        cursor.execute(
            "SELECT username,password FROM users WHERE username = ? AND password = ?",
            (
                username,
                password,
            ),
        )
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session["loggedin"] = True
            session["username"] = account[0]
            return redirect(url_for("profil"))
        else:
            # Account doesnt exist or username/password incorrect
            msg = "Incorrect username or password!"

    return render_template("registration/login.html", msg=msg)


@app.route("/logout/")
def logout():
    remove_data = ["username", "loggedin"]
    for data in remove_data:
        session.pop(data, None)

    return "bye"


@app.route("/games/")
def games():
    
    if is_logged():
        user = user_data()
        return render_template("games_folder/index.html",connected=True, user=user)
    return redirect(url_for("login"))



app.run(host="0.0.0.0", debug=True)
