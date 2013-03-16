from bs4 import BeautifulSoup
import urllib
import urllib2
import datetime

class ParseWeb():


	def open_schedule_page(self, values):
		#header
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1'
		headers = { 'User-Agent' : user_agent }

		url = 'http://schedule.psu.edu/search.cfm'

		search_values = values;

		data = urllib.urlencode(search_values)
		req = urllib2.Request(url, data, headers)
		response = urllib2.urlopen(req)
		the_page = response.read()

		return the_page

	def get_course_list(self):
		year = datetime.datetime.now().year
		values = { 'CECrseLoc' : 'All',
				   'CrseLoc' : 'UP::University Park',
				   'Semester' : 'FALL ' + str(year)}

		#parse the courses 
		html = self.open_schedule_page(values)
		soup = BeautifulSoup(html)
		select = soup.find('select',{'name' : 'course_abbrev'})
		option_text = select.findAll(text=True)
		option_text = option_text[1:]

		course_text = list()
		for option in option_text:
			if option != '\n':
				option = option.replace(u'\xa0',u'')
				course_text.append(option)

		return course_text