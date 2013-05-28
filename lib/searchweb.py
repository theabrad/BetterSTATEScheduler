import mechanize
import cookielib
import HTMLParser
import re
from bs4 import BeautifulSoup
import logging
import datetime

year = datetime.datetime.now().year

class SearchWeb():
	def select_semester(self, toggle):
		if toggle == 'fall':
			return "FALL " + str(year)
		elif toggle == 'spring':
			if datetime.datetime.now().month < 7:
				return "SPRING " + str(year)
			else:
				return "SPRING " + str(year+1)
		elif toggle == 'summer':
			return "SUMMER " + str(year)

	def split_course(self, course):
		seperator = ' - '
		if course.find(seperator)!=1:
			rest = course.split(seperator,1)[0]
		else:
			rest = course.split(' ',-1)[0]
		return rest.upper()

	def get_course_num(self, course):
		num = course.split(' ', -1)[-1]
		if num[0].isdigit():
			return num
		else:
			return 'no_num'
			
	def search_course(self, semester, course, num):
		# Browser
		br = mechanize.Browser()

		# Cookie Jar
		cj = cookielib.CookieJar()
		br.set_cookiejar(cj)

		# Browser options
		br.set_handle_equiv(True)
		br.set_handle_gzip(True)
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)

		# Follows refresh 0 but not hangs on refresh > 0
		br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

		# User-Agent
		br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1')]

		#open site
		r = br.open('http://schedule.psu.edu/searchNoJS.cfm')
		html = r.read()
		br.select_form(nr=0)

		br.form['CECrseLoc'] = ["All"]
		br.form['CrseLoc'] = ["UP::University Park"]
		br.form['Semester'] = [semester]
		br.form['course_abbrev'] = [course]
		if num!='no_num':
			br.form['course_num'] = [num]
		br.submit()

		response = br.response().read()

		return response

	def get_schedule(self,semester, course, num):
		html = self.search_course(semester, course, num)
		soup = BeautifulSoup(html)
		h = HTMLParser.HTMLParser()

		header = soup.find('h3',{'class':"floatleft"})

		for link in soup.findAll('a'):
			try:
				if link['href'].startswith('google') or link['href'].startswith('view'):
					link['href'] = 'http://schedule.psu.edu/'+link['href']
			except KeyError:
				pass

		
		for tag in soup.findAll('input'):
			tag.decompose()
	
		tables = soup.find_all('table')


		schedule = { 'header' : header,
					 'tables' : tables}

		return schedule
