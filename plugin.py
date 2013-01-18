import os
import re
import random

from string import letters

import webapp2

from google.appengine.ext import db

from data import *
from render import *


def randomAround(target,frequency):

	random_set=[]
	for i in range(frequency):
		random_set.append(int(target*random.uniform(0.9,1.1)))
	return random_set	

def formatted(input):
	input=input.strip()
	if(input.isdigit()):
		return input
	else:
		if(input.find(',') != -1):
			input=input.replace(',','')#lot more to be promoted

	return input

class KPI_random(PluginHandler):
	def get(self):
		self.render('kpi_random.html')
	def post(self):
		target=self.request.get('target')
		try:
			target=int(formatted(target))
		except:
			target=0
		data=[]
		if target:
			data=randomAround(target,5)
		self.render('kpi_random.html', target=target, data = data)

		

