#####
# Name   : fairfaxschooldelay.py
# Author : Simon Prickett
# Purpose: Determine if there is a school delay in Fairfax County VA
#####

from lxml import html
import requests
import schedule
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
		# Make sure today is not a school holiday
		return time.strftime('%x') not in [ 
			'01/19/15', '01/30/15', '02/02/15', 
			'02/16/15', '03/16/15', '03/30/15', 
			'03/21/15', '04/01/15', '04/02/15', 
			'04/03/15' ]
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
		# Normal school day no schedule change
		return 1
	elif (mainContentDiv.find('open two hours late') > -1):
		# School will open two hours later than usual
		return 2
	elif (mainContentDiv.find('close two hours early') > -1):
		# School opens at normal time with early dismissal
		return 3
	elif (mainContentDiv.find('will be closed today') > -1):
		# School is closed
		return 4
	else:
		# School open but evening and/or afternoon activities canceled
		return 5

#####
# Update the display
#
# schoolStatus:
# 0: Not a school day
# 1: No emergency, normal day
# 2: Two hour delay opening
# 3: Early closing, two hours ahead of normal
# 4: Closed all day
# 5: Open, but evening or afternoon activities canceled
#####
def updateDisplay():
	schoolStatus = 0

	if (isSchoolDay()):
		schoolStatus = getSchoolStatus()

	if (schoolStatus == 0):
		print "Not a school day."
	elif (schoolStatus == 1):
		print "Normal school day."
	elif (schoolStatus == 2):
		print "Two hour start delay."
	elif (schoolStatus == 3):
		print "Two hour early dismissal."
	elif (schoolStatus == 4):
		print "School closed today."
	elif (schoolStatus == 5):
		print "Extra curricular activities canceled."

#####
# Entry point, check school status over and over
#####
# TODO make the schedule more realistic
schedule.every(10).seconds.do(updateDisplay)
while True:
	schedule.run_pending()
	time.sleep(1)
