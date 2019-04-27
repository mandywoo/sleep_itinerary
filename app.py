from flask import Flask, render_template, request, url_for
import sqlite3
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
    # database.insert_users_data(database.get_database_file(), user, pw)
    return "Good luck with your webserver!"

# table list
timeList = []
for i in range(0, 37):
	if i % 2 == 0:
		timeList.append(str(int(6 + (i/2))) + ":00 am") if int(6 + i/2) <= 12 else timeList.append(str(int(6 + (i/2) - 12)) + ":00 pm")
	else:
		if int(6 + (i//2)) <= 12:
			timeList.append(str(6 + (i//2)) + ":30 am")
		else:
			timeList.append(str(6 + (i//2) - 12) + ":30 pm")

@app.route("/schedule")
def schedule():
    return render_template("schedule.html", len = len(timeList), timeList = timeList) 
    #return render_template("schedule.html")

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