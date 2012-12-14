import os
import re
from string import letters

import webapp2

from google.appengine.ext import db

from data import *
from render import *


class KPI_random(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("welcome to KPI_random")
