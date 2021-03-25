# New Automated System Engineers Reporting (N.A.S.E.R)

- [Installation](https://github.com/michal-minarik/naser#installation)
- [Getting Started](https://github.com/michal-minarik/naser#getting-started)
- [Customize Localization](https://github.com/michal-minarik/naser#customize-localization)
- [Tag events in your calendar](https://github.com/michal-minarik/naser#tag-events-in-your-calendar)
- [Input File Structure](https://github.com/michal-minarik/naser#input-file-structure)
- [Advanced Parameters](https://github.com/michal-minarik/naser#advanced-parameters)

# Demo

Here is a demo video how it works: https://vimeo.com/528747590 

# Known issues

- As SFDC is changing the UI quite often, sometimes script cannot correctly autodetect if you are using SFDC Lightning or the old classic SDFC. To mitigate this issue, before running the script switch you SFDC to classic manually.
- You must be connected to VPN - script cannot continue if Workspace ONE Access prompts for RSA MFA.
- The script also works with your username and password. If you have certificate imported to Firefox is won't be able to log you in.

# Installation

## Install Python

Check that you are running a Python on your machine. Open a terminal and execute:

```bash
python -V

Python 3.8.5
```

If you don't have Python on your machine install it by following the official documentation: https://www.python.org/downloads/

If you are running 2.X version of Python upgrade it. 

NOTE: It might be, that you have python 3.X on your machine already installed, but it might be behind the python3 command. Try: 

```bash
python3 -V

Python 3.8.5
```

If it works for you just use command python3 instead of python and continue with the setup.

## Install pip

pip is package manager we will need to download and install a couple of third party libraries for Python in order for our script to work.

You can check if you have a pip installed:

```bash
python -m pip --version

pip 20.2.4 from /usr/local/lib/python3.8/site-packages/pip (python 3.8)
``` 

If you don't have pip installed run following:

```bash 
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
``` 

## Install required python libraries

Check if you have pandas module installed:

```bash
pip list | grep pandas

pandas            1.1.4
```

If not run this command:

```bash 
pip install pandas
``` 

Check if you have selenium module installed:

```bash
pip list | grep selenium

selenium          3.141.0
```

If not run this command:

```bash 
pip install selenium
``` 

Check if you have openpyxl module installed:

```bash
pip list | grep openpyxl

openpyxl          3.0.6
```

If not run this command:

```bash 
pip install openpyxl
``` 

Check if you have requests module installed:

```bash
pip list | grep requests

requests          2.25.1
```

If not run this command:

```bash 
pip install requests
``` 

Check if you have icalendar module installed:

```bash
pip list | grep icalendar

icalendar          4.0.7
```

If not run this command:

```bash 
pip install icalendar
``` 

## Install Firefox driver for selenium

Assuming you have Firefox on your computer the reporting script will need driver to control the browser.

Download the lastest driver here: https://github.com/mozilla/geckodriver/releases

Whereever you will save the Firefox driver you will need to reference it in you PATH variable. For example if the file is in /Users/mminarik/python directory I would need to add this line into my terminal configuration file (~/.bash_profile).

```bash
export PATH="/Users/mminarik/python:$PATH"
```

After that you will need to close and reopen your terminal window. You can verify you did it correctly by finding the path in the output of this command:

```bash
echo $PATH | tr ":" "\n"

/Users/mminarik/python
/usr/local/opt/libpq/bin
/usr/local/Cellar/python/3.6.5_1/Frameworks/Python.framework/Versions/3.6/bin
/usr/local/sbin
/usr/local/bin
/usr/bin
/bin
/usr/sbin
/sbin
/Applications/VMware Fusion.app/Contents/Public
/Library/Apple/usr/bin
/Library/Frameworks/Mono.framework/Versions/Current/Commands
```

And you should also see this:

```bash
geckodriver -V 

geckodriver 0.28.0 (c00d2b6acd3f 2020-11-03 16:29 +0200)

The source code of this program is available from
testing/geckodriver in https://hg.mozilla.org/mozilla-central.

This program is subject to the terms of the Mozilla Public License 2.0.
You can obtain a copy of the license at https://mozilla.org/MPL/2.0/.
```

## Clone this repository

You will need multiple files in a single directory. The easiest way how to get this done is to clone this git repository. To do so run this command:

```git clone https://github.com/michal-minarik/naser.git```

If you don't have git installed on your machine follow the official docs to get it.

## Prepare the config.json

Make a copy of config_sample.json which comes within the repository and save it as config.json.

## Publish your O365 calendar

If you want to use the functionality to export the calendar and prepopulate the import file, you must share/publish your calendar. Login to you web Outlook - https://outlook.office.com. Go to Settings and "View all Outlook settings" section.

In this section navigate to Calendar > Shared Calendars. Here in the section "Publish a calendar" select your work calendar and publish it with the permission "Can view all details". Click publish. Copy the ICS link that has been generated for you.

Paste this link to the config.json file as a ics_url parameter.

# Getting started

## Prepare input file

When you cloned the repository a sample file sample_input.xlsx was created for you. Rename/duplicate this file and name it input.xlsx, keep it in the same directory. Now you can input your activities into this file.

Follow the structure from the sample file and [the input file structure](https://github.com/michal-minarik/naser#input-file-structure)

## Basic usage

You are all set to run the script. Navigate to the directory where you cloned the repository and execute:

```bash
python naser.py

 + New Automated System Engineers Reporting (N.A.S.E.R) version 1.2.1
 + Is your Excel ready to be imported? y
 + 208 tasks will be imported to SFDC
 + Autodetected username is: mminarik
 + Your VMware password:
```

It will autodetect your username and prompts for a password. This password is your domain password.

That's it. Now the script will open a controlled Firefox browser and load all tasks. Once it's done you will see the message:

```bash
Reporting done
```

## Calendar export

If you want to export your O365 calendar you need to run the script with additional arguments.

```bash
python naser.py --read-calendar true --start-date 2021-02-01 --end-date 2021-03-01

 + New Automated System Engineers Reporting (N.A.S.E.R) version 1.2.1
 + Downloading your calendar file from O365
 + Processing your calendar entries
 + Exporting data to input.xlsx file
 + Is your Excel ready to be imported? y
 + 208 tasks will be imported to SFDC
 + Autodetected username is: mminarik
 + Your VMware password:

```

This will export your calendar (see section Publish your O365 calendar) for necesary configuration.

The start and end date parameters are always in the YYYY-MM-DD format.

# Customize localization

Because your SFDC might talk in different language you must set up your localization settings correctly in the config.json file. There are two main points where the automation typically fails.

**Date format**

When importing tasks you will see in the Firefox window error: Invalid Date.

To fix this issue, open the config.json file and change this line to match your SFDC date format:

```"date_format": "%d.%m.%Y",```

**Decimal separator**

When importing tasks you will see in the Firefox window error: Invalid Number.

To fix this issue, open the config.json file and change this line to match your SFDC numbering format:

```"decimal_separator": ","```

# Tag events in your calendar

When using the calendar export feature you can add a special tag to the body of your event which will then be recognized, pnaserd and exported automatically to the input.xlsx file.

Here are the options for internal activity:

```#i:<HERE WILL BE YOUR ACTIVITY TYPE>:n/a:n/a#``` so for example: ```#i:Meetings:n/a:n/a#```

Here are the options for EMEA SE activity:

```#e:<HERE WILL BE YOUR ACTIVITY TYPE>:Account:<ACCOUNT NAME FROM SFDC>#``` so for example: ```#e:Workshop:Account:Dell Computers Czech Republic#```

or you can link to opportunity:

```#e:<HERE WILL BE YOUR ACTIVITY TYPE>:Opportunity:<OPPORTUNITY NAME FROM SFDC>#``` so for example: ```#e:Demo:Opportunity:CZ/RS/.../MDM#```


# Input file structure

### Fields for EMEA SE Activity

Following fields are mandatory and must be filled:

| Field  | Decription | Value | 
| ------------- | ------------- | ------------- |
| date  | Activity date | Date |
| activity  | Internal or normal activity definition  | EMEA SE Activity |
| type  | Activity type  | [EMEA SE Activity - type values](https://github.com/michal-minarik/naser#emea-se-activity---type-values) |
| subject  | Activity subject  | Text |
| notes  | Notes / Comments  | Text (Optional) |
| next_step  | Next step  | Text (Optional) |
| related_object  | Related to SFDC type  | [EMEA SE Activity - related_object values](https://github.com/michal-minarik/naser#emea-se-activity---related_object-values) |
| related_to  | Related to SFDC resource  | Text (exact name of the SFDC resource e.g. opportunity name) |
| activity_category  | Activity Category  | Values in SFDC (Optional) |
| solution  | Solution  | Values in SFDC (Optional) |
| solution_product  | Product  | Values in SFDC (Optional) |
| hours  | Worked hours  | Integer |
| status  | Task status  | [EMEA SE Activity - status values](https://github.com/michal-minarik/naser#emea-se-activity---status-values)  |

#### EMEA SE Activity - type values

- Account Management
- App Domain Architecture
- Beta Program / Mgmt
- Customer Adopt
- Customer Reference
- Dell Technologies Play
- Demo
- DICE
- DOMINO
- Champions - SME program
- Live Optics
- Non VMware Marketing Event (Inc. VMUG)
- Partner Management
- Partner Presales Centre
- PoC / PoV
- Post Sales Support
- PowerBlocks
- Pre-Sales PSO / Scoping
- Pre-Sales Support
- Presentation
- Projects
- RFI / RFP / RFQ
- Roadmap
- Self Driving Ops
- Trial
- VBC
- Virtual Customer Lab
- VMware Marketing Events
- Workshop

#### EMEA SE Activity - related_object values

- Account
- Opportunity

#### EMEA SE Activity - status values

- Not Started
- In Progress
- Completed

### Fields for SE Internal Activity

Following fields are mandatory and must be filled:

| Field  | Decription | Value | 
| ------------- | ------------- | ------------- |
| date  | Activity date | Date |
| activity  | Internal or normal activity definition  | SE Internal Activity |
| type  | Activity type  | [SE Internal Activity - type values](https://github.com/michal-minarik/naser#se-internal-activity---type-values) |
| subject  | Activity subject  | Text |
| notes  | Notes / Comments  | Text (Optional) |
| hours  | Worked hours  | Integer |
| status  | Task status  | [SE Internal Activity - status values](https://github.com/michal-minarik/naser#se-internal-activity---status-values)  |


#### SE Internal Activity - type values

- Admin
- Conferences
- Demo
- Champions - SME program
- Internal Enablement
- Internal Event Support
- Management or Team Activities
- Meetings
- Paid Time Off, Holiday
- POC
- Recruiting
- Service Learning
- Training

#### SE Internal Activity - status values

- Not Started
- In Progress
- Completed


# Advanced parameters

If the script does not detect your username correctly (for example you are not running corporate image), you can force a username prompt:

```bash
python naser.py --prompt-username
```