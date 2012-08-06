import os
import json
from tornado import wsgi
from tornado.options import options
from app import routes, settings


    
application = wsgi.WSGIApplication(routes, **settings)
