from tornado import web
from tornado.options import options, define
import datetime
import json
from parseweb import ParseWeb
from searchweb import SearchWeb 

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

class Search(web.RequestHandler):
    def post(self):
        course = self.get_argument("course")
        sem = self.get_argument("toggle")
        course = self.split_course(course)
        semester = self.select_semester(sem)

        search = SearchWeb()
        schedule = search.get_schedule(semester, course)

        self.render("schedule.html", schedule=schedule)

    def select_semester(self, toggle):
        if toggle=='fall':
            return "FALL " + str(year)
        elif toggle=='spring':
            if datetime.datetime.now().month < 7:
                return "SPRING " + str(year)
            else:
                return "SPRING " + str(year+1)
        elif toggle=='summer':
            return "SUMMER " + str(year)

    def split_course(self, course):
        seperator = ' - '
        rest = course.split(seperator,1)[0]
        return rest


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
]

