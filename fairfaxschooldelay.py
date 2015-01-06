#####
# Name   : fairfaxschooldelay.py
# Author : Simon Prickett
# Purpose: Determine if there is a school delay in Fairfax County VA
#####

from lxml import html
import requests
import time

#####
# Is it a school day today?
#####
def isSchoolDay():
	# Simplistic, should really consult a school 
	# calendar page for holidays and also as some 
	# may change due to snow make up days
	currentDay = time.strftime('%A')
	if (currentDay == 'Saturday' or currentDay == 'Sunday'):
		return False
	else:
		schoolHolidays = [ '01/19/15', '01/30/15', '02/02/15', '02/16/15', 
		                   '03/16/15', '03/30/15', '03/21/15', '04/01/15', 
		                   '04/02/15', '04/03/15' ]
		return time.strftime('%x') not in schoolHolidays

#####
# Get the page data from the school system
#####
def getWebPage():
	r = requests.get('http://www.fcps.edu/news/emerg.shtml')
	if (r.status_code == 200):
		return html.fromstring(r.text)
	else:
		print 'Error getting school system webpage!'

#####
# Get the current status of the school system
#####
def getSchoolStatus():
	htmlTree = getWebPage()
	mainContentDiv = htmlTree.xpath('//div[@id="mainContent"]/p/strong/text()')[0]
	
	if (mainContentDiv.find('no emergency announcements') > -1):
		return 1
	else:
		# TODO is it a late start, early release or snow day
		return 2

#####
# Entry point
#
# schoolStatus:
# 0: Not a school day
# 1: No emergency
# 2: Some sort of emergency TODO define further
#####
schoolStatus = 0

if (isSchoolDay()):
	schoolStatus = getSchoolStatus()

if (schoolStatus == 0):
	print "No school today."
elif (schoolStatus == 1):
	print "Normal school day."
elif (schoolStatus == 2):
	print "Some sort of schedule change."
