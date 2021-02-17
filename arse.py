#
# Automated Reporting for System Engineers (A.R.S.E)
# by Michal Minarik (mminarik@vmware.com)
# version 1.1
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
print('  Automated Reporting for System Engineers (A.R.S.E.) version 1.0')
print('*******************************************************************')

parser = argparse.ArgumentParser()
parser.add_argument("--limit-start")
parser.add_argument("--limit-end")
parser.add_argument("--calendar-file")
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

if args.calendar_file != None:

	xtree = et.parse(args.calendar_file)
	xroot = xtree.getroot()

	data = []

	for node in xroot.iter('appointment'):

		activity = ''
		activityType = ''
		related_object = ''
		related_to = ''

		try:
			summary = node.find('OPFCalendarEventCopySummary').text.strip()
		except AttributeError:
			summary = ''

		start = pd.to_datetime(node.find('OPFCalendarEventCopyStartTime').text)
		end = pd.to_datetime(node.find('OPFCalendarEventCopyEndTime').text)

		try:
			description = node.find('OPFCalendarEventCopyDescriptionPlain').text
		except AttributeError:
			description = ''

		# Calculate the duration and round to half hours
		duration = round(((end - start).total_seconds() / 3600) * 2) / 2

		if description:
			# Sanitize input for RegEx
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

		# Skip items before selected date
		if args.limit_start:
			limitStart = pd.to_datetime(args.limit_start)
			if (start <= limitStart):
				continue

		# Skip items after selected date
		if args.limit_end:
			limitEnd = pd.to_datetime(args.limit_end)
			if (start >= limitEnd):
				continue

		data.append([start, activity, activityType, summary, duration, related_object, related_to, 'Completed'])

	df = pd.DataFrame(data, columns = ['date', 'activity', 'type', 'subject', 'hours', 'related_object', 'related_to', 'status'])

	df.to_excel('input.xlsx', index=False)

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
#browser = webdriver.Firefox()

# Use Selenuim container from defined host
browser = webdriver.Remote(
   command_executor=str(configs['worker']) ,
   desired_capabilities={'browserName': 'firefox'})

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

		dateField = browser.find_element_by_id("tsk4")
		dateField.send_keys(row.date.strftime(str(configs['date_format'])))

		relatedObjectSelect = Select(browser.find_element_by_id('tsk3_mlktp'))
		relatedObjectSelect.select_by_visible_text(row.related_object)

		relatedToField = browser.find_element_by_id("tsk3")
		relatedToField.send_keys(row.related_to)

		activityTypeSelect = Select(browser.find_element_by_id('00N80000004k1L2'))
		activityTypeSelect.select_by_value(row.type)

		statusSelect = Select(browser.find_element_by_id('tsk12'))
		statusSelect.select_by_value(row.status)

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
