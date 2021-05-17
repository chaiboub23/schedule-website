from flask import Flask, render_template, request, redirect
from flask_cors import CORS

from icalendar import Calendar, Event
import re
import urllib.request
from datetime import datetime, timedelta
from pytz import timezone

app = Flask(__name__)
CORS(app)

temp = []
assignments = {}
calendar = []
exp = re.compile(r'C([1-8])')
s = '-03:00'

@app.route('/')
def home():
    if request.cookies.get('text'):
        return redirect('/schedule')
    return render_template('index.html')

@app.route('/schedule')
def render_schedule():
    url = request.cookies.get('text')
    if "webcal" in url:
        url = url.replace('webcal', 'https')
        print(url)
        with urllib.request.urlopen(url) as f:
            data = f.read().decode('utf-8')
        temp = []
        assignments = {}
        calendar = []
        cal = Calendar.from_ical(data)
        for component in cal.walk():
            if component.name == "VEVENT":
                summary = str(component.get("summary"))
                if ":" in summary or "Test" in summary:
                    continue
                else:
                    # If event block get date the block starts
                    t = component.get('dtstart').dt
                    if "Day" in summary or exp.search(summary) or "Break" in summary or "Sleep-In" in summary or "Advisor" in summary or "Head of School" in summary:
                        continue
                    else:
                        try:
                            if t.date() == datetime.now().date():
                                print(summary)
                                time = str(t.time())
                                time = time.replace(s, '')
                                temp.append(summary)
                                temp.append(time)
                                calendar.append(temp)
                                temp = []
                        except TypeError:
                            continue
                        except AttributeError:
                            continue
    return render_template("schedule.html", calendar=calendar)

@app.route('/assignments')
def render_assignments():
    url = request.cookies.get('text')
    if "webcal" in url:
        url = url.replace('webcal', 'https')
        print(url)
        with urllib.request.urlopen(url) as f:
            data = f.read().decode('utf-8')
        temp = []
        assignments = {}
        calendar = []
        cal = Calendar.from_ical(data)
        for component in cal.walk():
            if component.name == "VEVENT":
                summary = str(component.get("summary"))
                if ":" in summary or "Test" in summary:
                    # If assignment get date the assignment is due
                    t = (component.get('dtend').dt - timedelta(days=1))
                    time = str(t)
                    if t < datetime.now().date():
                        continue
                    assignments[summary] = time
                else:
                    continue
    return render_template("assignments.html", assignments=assignments)

assignments = {}

calendar = []

@app.route('/todo-list')
def render_todolist():
    return render_template("todos.html")
