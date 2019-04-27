from flask import Flask, render_template, request
import database


app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def home():
    user = request.form["username"]
    pw = request.form["password"]
    print("user logged in with: " + user + ", " + pw)


    database.insert_users_data(database.get_database_file(), user, pw)

    return "Good luck with your webserver!"


app.run()


