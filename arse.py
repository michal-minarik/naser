#
# Automated Reporting for System Engineers (A.R.S.E)
# by Michal Minarik (mminarik@vmware.com)
# version 1.2
#

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import xml.etree.ElementTree as et 
import pandas as pd
import getpass
import argparse
import re
import json
import time
import icalendar
import requests

# Class for checking if SDFC was loaded (either Lighning or Classic)
class sfdc_is_loaded_class(object):
	def __call__(self, driver):
		element = driver.find_element_by_xpath("/html/body")
		classes = element.get_attribute("class")
		if classes != '':
			if "desktop" in classes:
				return element
			elif "sfdcBody" in classes:
				return element
			else:
				return False


print('\n*******************************************************************')
print('  Automated Reporting for System Engineers (A.R.S.E.) version 1.2')
print('*******************************************************************')

parser = argparse.ArgumentParser()
parser.add_argument("--start-date")
parser.add_argument("--end-date")
parser.add_argument("--read-calendar")
parser.add_argument("--prompt-username")
args = parser.parse_args()

# Read configuration JSON
with open('config.json', 'r') as configFile:
    data = configFile.read()

# Parse JSON file
configs = json.loads(data)

#
# Calendar load
#

if args.read_calendar != None:

	print(" + Downloading your calendar file from O365")

	# Get the calendar from subscribed url
	icsFile = requests.get(configs['ics_url']).text

	print(" + Processing the calendar file")

	gcal = icalendar.Calendar.from_ical(icsFile)

	data = []

	for component in gcal.walk():
		if component.name == "VEVENT":

			activity = ''
			activityType = ''
			related_object = ''
			related_to = ''

			summary = component.get('summary').strip()

			start = component.get('dtstart').dt
			end = component.get('dtend').dt
			duration = round(((end - start).total_seconds() / 3600) * 2) / 2

			description = component.get('description')

			# Process the description
			if description:
				description = description.replace("\u2028", "")

				matches = re.match(r"^#(e|i):(\w+):(Account|Opportunity):(.+)#$", description, re.MULTILINE)
				if matches:
					if matches.groups()[0] == "e":
						activity = "EMEA SE Activity"
					elif matches.groups()[0] == "i":
						activity = "SE Internal Activity"
					activityType = matches.groups()[1]
					related_object = matches.groups()[2]
					related_to = matches.groups()[3]

			data.append([start, activity, activityType, summary, '', '', related_object, related_to, '', '', '', duration, 'Completed'])

	df = pd.DataFrame(data, columns = ['date', 'activity', 'type', 'subject', 'notes', 'next_step', 'related_object', 'related_to', 'activity_category', 'solution', 'solution_product', 'hours', 'status']) 

	df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', utc=True) 

	# Filter results based on dates
	if args.start_date and args.end_date:
		filtered_df = df.loc[(df['date'] >= args.start_date) & (df['date'] < args.end_date)] 
	else:
		filtered_df = df

	filtered_df['date'] = filtered_df['date'].dt.tz_localize(None)

	print(" + Exporting data to input.xlsx file")

	filtered_df.to_excel('input.xlsx', index=False)
#
# Wait for confimation
#

print("Is your Excel ready to be imported?")
input()

#
# Import to SFDC
#

df = pd.read_excel('input.xlsx')

print('\nTasks to be reported:')
print('\n------------')
print(df)
print('------------\n')

# Get the username and password
if args.prompt_username:
	print('Your VMware username:')
	username = input()
else:
	username = getpass.getuser()
	print('Your VMware username: ' + username)
password = getpass.getpass()

# Open Firefox and start login to SFDC
browser = webdriver.Firefox()
wait = WebDriverWait(browser, 30)
browser.get('https://vmware.my.salesforce.com')

ssoButton = browser.find_element_by_xpath("//div[@id='idp_section_buttons']/button[2]")
ssoButton.click()

# Sign in using username/password to Workspace ONE
wait.until(EC.presence_of_element_located((By.ID, "username")))

usernameField = browser.find_element_by_id("username")
usernameField.send_keys(username)
passwordField = browser.find_element_by_id("password")
passwordField.send_keys(password)

signInButton = browser.find_element_by_id("signIn")
signInButton.click()

lightningNotificationDismissed = False

# Wait for SFDC to load
wait.until(sfdc_is_loaded_class())

# Check for SFDC Lightning
matches = re.match(r".*lightning.*", browser.current_url)
if matches:
	print("Lightning detected - Switching to SFDC Classic")

	browser.implicitly_wait(10)

	profileIcon = browser.find_element_by_xpath("/html/body/div[4]/div[1]/section/header/div[2]/span/div[2]/ul/li[8]/span/button/div/span[1]/div")
	profileIcon.click()

	switchToClassicLink = browser.find_element_by_xpath("/html/body/div[4]/div[2]/div[2]/div[1]/div[1]/div/div[5]/a")
	switchToClassicLink.click()

	# wait.until(EC.presence_of_element_located((By.ID, "lightningFeedbackPage:feedbackForm")))

	lightningNotificationDismissed = True

# Wait classic SFDC to load
wait.until(EC.title_is("Salesforce - Unlimited Edition"))

for index, row in df.iterrows():

	print("Processing task [" + str(index + 1) + "/" + str(len(df)) + "]")

	if row.activity == "EMEA SE Activity":

		# Go to "non-lightning" new task creation form
		browser.get('https://vmware.my.salesforce.com/00T/e?retURL=%2Fapex%2FSFA_SEActivitiesTab&RecordType=01234000000QF7y&ent=Task')

		# Dismiss the SFDC switch to Lighning notification. The dialog popup blocks screen and automatic select does not work.
		if lightningNotificationDismissed is False:

			wait.until(EC.presence_of_element_located((By.ID, "lexNoThanks")))
			
			lightningNotificationQuestionButton = browser.find_element_by_id("lexNoThanks")
			lightningNotificationQuestionButton.click()

			wait.until(EC.presence_of_element_located((By.ID, "lexSubmit")))
			
			lightningNotificationCloseButton = browser.find_element_by_id("lexSubmit")
			lightningNotificationCloseButton.click()

			lightningNotificationDismissed = True

		# Fill the form
		subjectField = browser.find_element_by_id("tsk5")
		subjectField.send_keys(row.subject)

		if not pd.isna(row.notes):
			notesField = browser.find_element_by_id("tsk6")
			notesField.send_keys(row.notes)

		if not pd.isna(row.next_step):
			nextStepField = browser.find_element_by_id("00N80000004k1LI")
			nextStepField.send_keys(row.next_step)

		dateField = browser.find_element_by_id("tsk4")
		dateField.send_keys(row.date.strftime(str(configs['date_format'])))

		relatedObjectSelect = Select(browser.find_element_by_id('tsk3_mlktp'))
		relatedObjectSelect.select_by_visible_text(row.related_object)

		relatedToField = browser.find_element_by_id("tsk3")
		relatedToField.send_keys(row.related_to)

		if not pd.isna(row.activity_category):
			activityCategorySelect = Select(browser.find_element_by_id('00N80000004oGaG'))
			activityCategorySelect.select_by_visible_text(row.activity_category)

		activityTypeSelect = Select(browser.find_element_by_id('00N80000004k1L2'))
		activityTypeSelect.select_by_value(row.type)

		statusSelect = Select(browser.find_element_by_id('tsk12'))
		statusSelect.select_by_value(row.status)

		if not pd.isna(row.solution):
			solutionSelect = Select(browser.find_element_by_id('00N80000004oGaR'))
			solutionSelect.select_by_visible_text(row.solution)

		if not pd.isna(row.solution_product):
			productSelect = Select(browser.find_element_by_id('00N80000004oGaL'))
			productSelect.select_by_visible_text(row.solution_product)

		workHoursField = browser.find_element_by_id("00N80000004k1Mo")
		workHoursField.send_keys(str(row.hours).replace(".", str(configs['decimal_separator'])))

		# Submit
		submitButton = browser.find_element_by_xpath("/html/body/div[1]/div[3]/table/tbody/tr/td[2]/form/div/div[3]/table/tbody/tr/td[2]/input[1]")
		submitButton.click()

		# Wait for the form to be fully submited (TODO: Create some condition and remove the explicit wait)
		browser.implicitly_wait(10) # seconds

	elif row.activity == "SE Internal Activity":

		# Go to "non-lightning" new task creation form
		browser.get('https://vmware.my.salesforce.com/00T/e?retURL=%2Fapex%2FSFA_SEActivitiesTab&RecordType=01280000000BY0b&ent=Task')

		# Dismiss the SFDC switch to Lighning notification. The dialog popup blocks screen and automatic select does not work.
		if lightningNotificationDismissed is False:

			wait.until(EC.presence_of_element_located((By.ID, "lexNoThanks")))
			
			lightningNotificationQuestionButton = browser.find_element_by_id("lexNoThanks")
			lightningNotificationQuestionButton.click()

			wait.until(EC.presence_of_element_located((By.ID, "lexSubmit")))
			
			lightningNotificationCloseButton = browser.find_element_by_id("lexSubmit")
			lightningNotificationCloseButton.click()

			lightningNotificationDismissed = True
		
		# Fill the form
		subjectField = browser.find_element_by_id("tsk5")
		subjectField.send_keys(row.subject)

		if not pd.isna(row.notes):
			notesField = browser.find_element_by_id("tsk6")
			notesField.send_keys(row.notes)

		dateField = browser.find_element_by_id("tsk4")
		dateField.send_keys(row.date.strftime(str(configs['date_format'])))
		
		activityTypeSelect = Select(browser.find_element_by_id('00N80000004k1L2'))
		activityTypeSelect.select_by_value(row.type)

		workHoursField = browser.find_element_by_id("00N80000004k1Mo")
		workHoursField.send_keys(str(row.hours).replace(".", str(configs['decimal_separator'])))

		statusSelect = Select(browser.find_element_by_id('tsk12'))
		statusSelect.select_by_value(row.status)

		# Submit
		submitButton = browser.find_element_by_xpath("/html/body/div[1]/div[3]/table/tbody/tr/td[2]/form/div/div[3]/table/tbody/tr/td[2]/input[1]")
		submitButton.click()

		# Wait for the form to be fully submited (TODO: Create some condition and remove the explicit wait)
		browser.implicitly_wait(10) # seconds
	
	else:
		print("Item cannot be logged due to invalid value of field 'activity'")

print("\nReporting in done!")

