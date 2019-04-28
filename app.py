from flask import Flask, render_template, request, url_for
import sqlite3
from sqlite3 import Error
import database
import os
import random

TASK_LIST = []

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
    return render_template("sleep.html", len = len(timeList), timeList = timeList)

@app.route("/sleep", methods=["POST"])
def sleep_box():
    print('hi')
    sleep_hours = request.form["hours"]
    bedtime = request.form["bedtime"]
    wakeup_time = request.form["wakeup_time"]

    return render_template("task.html", len = len(timeList), timeList = timeList)
    # return render_template("schedule.html", len = len(timeList), timeList = timeList) 

@app.route("/schedule")
def schedule():
    return render_template("schedule.html", len = len(timeList), timeList = timeList, colorList = colorList) 
    #return render_template("schedule.html")

@app.route("/task", methods=["POST"])
def task_box():
    task_title = request.form["task_title"]
    from_time = request.form["from_time"]
    to_time = request.form["to_time"]
    task_description = request.form["description"]
    TASK_LIST.append((from_time, to_time, task_title, task_description))
    hex = '#{:02x}{:02x}{:02x}'.format(*random.sample(range(256), 3))
    return render_template("schedule.html", len = len(timeList), timeList = timeList, task_list = TASK_LIST, hex = hex) 

    # return render_template("task.html")

def calc_end_sleep_time(sleep_hours, start):
    start_hour, ampm = start.split()
    hour, minutes = start_hour.split(':')
    end_hour = int(hour) + int(sleep_hours)    
    if end_hour > 12:
        if ampm == 'am':
            ampm = 'pm'
        elif ampm == 'pm':
            ampm = 'am'
    return str(end_hour) + ':' + str(minutes) + ' ' + str(ampm)



# table list
timeList = []
for i in range(0, 48):
    if i % 2 == 0:
        time = int(6 + i/2)
        if time == 24:
            timeList.append(str(time - 12) + ":00 am")
        elif time == 12:
            timeList.append(str(time) + ":00 pm")
        elif time < 12:
            timeList.append(str(time) + ":00 am")
        elif time - 12 < 12:
            timeList.append(str(time - 12) + ":00 pm")
        else:
            timeList.append(str(time - 24) + ":00 am")
    else:
        time = int(6 + (i//2))
        if time == 24:
            timeList.append(str(time - 12) + ":30 am")
        elif time == 12:
            print(time)
            timeList.append(str(time) + ":30 pm")
        elif time < 12:
            timeList.append(str(time) + ":30 am")
        elif int((6 + (i//2) - 12)) < 12:
            timeList.append(str(time - 12) + ":30 pm")
        else:
            timeList.append(str(time - 24) + ":30 am")



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