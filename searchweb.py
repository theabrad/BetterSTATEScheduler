import mechanize
import cookielib
import HTMLParser
import re
from bs4 import BeautifulSoup
import logging

class SearchWeb():
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
