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
	# <div id="mainContent"><p><strong>There are no emergency announements at this time. </strong></p>
	mainContentDiv = htmlTree.xpath('//div[@id="mainContent"]/p/strong/text()')[0]
	
	if (mainContentDiv.find('no emergency announcements') > -1):
		# Normal school day no schedule change
		return 0

	# OK so it's not a normal day, let's find a condition... and
	# there might be multiple announcements
	mainContentParagraphs = htmlTree.xpath('//div[@id="mainContent"]/p')
	for p in mainContentParagraphs:
		txt = p.text_content()
		i =  txt.find('Condition ')
		if (i > -1):
			# Found it, which condition is it?
			# Possibilities are listed here: http://www.fcps.edu/news/conditions.shtml
			if (txt.find('Condition 1') > -1):
				# Condition 1: All day closing (inc offices)
				return 1
			elif (txt.find('Condition 2') > -1):
				# Condition 2: All day closing
				return 2
			elif (txt.find('Condition 3') > -1):
				# Condition 3: 2 hour delay
				return 3
			elif (txt.find('Condition 4') > -1):
				# Condition 4: 2 hour early dismissal
				return 4
			elif (txt.find('Condition 5') > -1):
				# Condition 5: closed with delayed office opening
				return 5
			elif (txt.find('Condition 6') > -1):
				# Condition 6: afternoon and evening activities canceled
				return 6
			elif (txt.find('(Condition 7') > -1):
				# Condition 7: evening activities canceled
				return 7

	# If we got here we have no idea what is going on
	return 99

#####
# Update the display
#
#####
def updateDisplay():
	# Treating status -1 as not a school day
	schoolStatus = -1 

	if (isSchoolDay()):
		schoolStatus = getSchoolStatus()

	if (schoolStatus == 0):
		# School day and school is open
		print "Condition " + str(schoolStatus) + " school is OPEN"
	elif (schoolStatus == 1 or schoolStatus == 2 or schoolStatus == 5):
		# School is closed all day
		print "Condition " + str(schoolStatus) + " school is CLOSED"
	elif (schoolStatus == 3):
		print "Condition " + str(schoolStatus) + " school is DELAYED 2 HOURS"
	elif (schoolStatus == 4):
		print "Condition " + str(schoolStatus) + " school will CLOSE 2 HOURS EARLY"
	elif (schoolStatus == 6):
		print "Condition " + str(schoolStatus) + " school is OPEN with AFTERNOON AND EVENING ACTIVITIES CANCELED"
	elif (schoolStatus == 7):
		print "Condition " + str(schoolStatus) + " school IS OPEN with EVENING ACTIVITIES CANCELED"
	else:
		print "Condition unknown, please check with the school system"

#####
# Entry point, check school status over and over
#####
# TODO make the schedule more realistic
schedule.every(30).seconds.do(updateDisplay)
while True:
	schedule.run_pending()
	time.sleep(1)
