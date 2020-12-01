# Automated Reporting for System Engineers (A.R.S.E.)

- [Installation](https://github.com/michal-minarik/arse#installation)
- [Getting Started](https://github.com/michal-minarik/arse#getting-started)
- [Advanced Parameters](https://github.com/michal-minarik/arse#advanced-parameters)

# Installation

## Install Python

Check that you are running a Python on your machine. Open a terminal and execute:

```bash
python -V

Python 3.8.5
```

If you don't have Python on your machine install it by following the official documentation: https://www.python.org/downloads/

If you are running 2.X version of Python upgrade it.

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

## Install selenium and pandas libraries

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

## Download the script

Download the arse.py script from this repository also download the sample_input.xlsx file and save as input.xlsx in the same directory where you have the script.

# Getting started

## Basic usage

You are all set to run the script. Navigate to the directory where you saved the script and execute:

```bash
python ./arse.py
```

The script will recap, what it will import into SFDC.


```bash
Tasks to be reported:

------------
        date      type      subject  hours related_object        related_to     status
0 2020-10-20  Workshop  Hello world      2        Account               ***  Completed
1 2020-10-21  Workshop  Hello world      2    Opportunity               ***  Completed
------------
```

Then it will autodetect your username and prompts for a password. This password is your domain password.

```bash
Your VMware username: ********
Password: 
```

Next step is to confirm you date/time format you SFDC is expecting. For example in my case, SFDC uses Czech date format 30.11.2020 so I am OK with the defaults and I can just hit enter. If you are using diffent format you will need to specify it.

```bash
Your SFDC date format (default: %d.%m.%Y):
```

That's it. Now the script will open a controlled Firefox browser and load all the tasks (as EMEA SE Activity taks). Once it's done you will see the message:

```bash
Reporting done
```

## Input file structure

### Fields for EMEA SE Activity

Following fields are mandatory and must be filled:

| Field  | Decription | Value | 
| ------------- | ------------- | ------------- |
| date  | Activity date | Date |
| activity  | Internal or normal activity definition  | EMEA SE Activity |
| type  | Activity type  | [EMEA SE Activity - type values](https://github.com/michal-minarik/arse#emea-se-activity---type-values) |
| subject  | Activity subject  | Text |
| hours  | Worked hours  | Integer |
| related_object  | Related to SFDC type  | [EMEA SE Activity - related_object values](https://github.com/michal-minarik/arse#emea-se-activity---related_object-values) |
| related_to  | Related to SFDC resource  | Text (exact name of the SFDC resource e.g. opportunity name) |
| status  | Task status  | [EMEA SE Activity - status values](https://github.com/michal-minarik/arse#emea-se-activity---status-values)  |

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
| type  | Activity type  | [SE Internal Activity - type values](https://github.com/michal-minarik/arse#se-internal-activity---type-values) |
| subject  | Activity subject  | Text |
| hours  | Worked hours  | Integer |
| status  | Task status  | [SE Internal Activity - status values](https://github.com/michal-minarik/arse#se-internal-activity---status-values)  |


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
python arse.py --prompt-username
```