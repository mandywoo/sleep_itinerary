from flask import Flask, render_template, request, url_for
import sqlite3
from sqlite3 import Error
import database
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def home():
    user = request.form["username"]
    pw = request.form["password"]
    print("user logged in with: " + user + ", " + pw)
    try:
        database.insert_users_data(database.get_database_file(), user, pw)
    except sqlite3.IntegrityError:
        # if the user already exists
        pass
    return render_template("sleep.html")

@app.route("/sleep", methods=["POST"])
def sleep_box():
    # sleep_hours = request.form["sleep_hours"]
    # bed_time = request.form["bedtime"]
    # wakeup_time = request.form["wakeup_time"]
    # print("user sleeps" + sleep_hours + "from:" + bed_time + "to" + wakeup_time)
 
    return "Go To Schedule!"


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
app.run()