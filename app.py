import sys
import datetime
import json
from lib.parseweb import ParseWeb
from lib.searchweb import SearchWeb
from flask import Flask, request, render_template, url_for

app = Flask(__name__)

year = datetime.datetime.now().year
COURSECACHE = {}


# Get the list of courses and store them in a cache
def cache_course_list():
    key = 'list'

    if key in COURSECACHE:
        course_list = COURSECACHE[key]
    else:
        parse = ParseWeb()
        course_list = parse.get_course_list()
        COURSECACHE[key] = course_list
    return course_list


@app.route("/")
def main_page():
    return render_template("home.html", year=year)

@app.route("/courses")
def get_courses():
    courses = cache_course_list()
    courses.sort()
    course_json = json.dumps(courses)
    return course_json

@app.route("/search", methods=['POST'])
def search():
    course_full = request.form['course']
    sem = request.form['toggle']

    search = SearchWeb()
    semester = search.select_semester(sem)
    course = search.split_course(course_full)
    num = search.get_course_num(course_full)

    try:
        schedule = search.get_schedule(semester, course, num)
        error=False
    except:
        schedule = search.get_schedule(semester, course, '')
        error=True

    return render_template("schedule.html", schedule=schedule, year=year, error=error)

@app.route("/about")
def about():
    return render_template("about.html", year=year)


if __name__ == '__main__':
    app.run()