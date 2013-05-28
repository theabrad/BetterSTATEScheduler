from tornado import web
from tornado.options import options, define
import sys
import datetime
import json
import re
import logging
from lib.parseweb import ParseWeb
from lib.searchweb import SearchWeb

define("port", default=8000, help="http port", type=int)
define("cookie_secret", default="not-much-of-a-secret")
define("debug", default=False, help="debug mode", type=bool)

year = datetime.datetime.now().year
COURSECACHE = {}
class MainPage(web.RequestHandler):
    def get(self):
        
        #values = year
            
        self.render("home.html", year=year)

class Courses(web.RequestHandler):
    def get(self):
        courses = self.cache_courselist()
        courses.sort()
        course_json = json.dumps(courses)
        self.write(course_json)

    def cache_courselist(self):
        key = 'list'

        if key in COURSECACHE:
            course_list = COURSECACHE[key]
        else:
            parse = ParseWeb()
            course_list = parse.get_course_list()
            COURSECACHE[key] = course_list
        return course_list

    def clear_cache(self):
        current_month = datetime.datetime.now().month
        prev_month = current_month
        if current_month != prev_month:
            COURSECACHE = {}

class Search(web.RequestHandler):
    def post(self):
        course_full = self.get_argument("course")
        sem = self.get_argument("toggle")

        search = SearchWeb()
        semester = search.select_semester(sem)
        course = search.split_course(course_full)
        num = search.get_course_num(course_full)

        try:
            schedule = search.get_schedule(semester, course, num) #semester course number
            error=False
        except:
            schedule = search.get_schedule(semester, course, '')
            error=True          

        self.render("schedule.html", schedule=schedule, year=year, error=error)

class StaticPages(web.RequestHandler):
    def get(self, page):
        if page=="about":
            self.render("about.html", year=year)
        else:
            self.write("Page not found")
        
        



settings = dict(
    template_path="templates",
    static_path="static",
    xsrf_cookies=False,                 #CHANGE MAYBE
    search_url = "/search",
    cookie_secret=options.cookie_secret,
    debug=options.debug,
)

routes = [
    (r"/", MainPage),
    (r"/courses", Courses),
    (r"/search", Search),
    (r"/pages/(.*)", StaticPages),
]

