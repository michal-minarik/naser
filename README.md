# Automatic Reporting for System Engineers (A.R.S.E.)


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

Just run those two commands:

```bash 
pip install pandas
``` 

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

You are all set to run the script. Navigate to the directory where you saved the script and execute:

```bash
python ./arse.py
```

The script will recap, what it will import into SFDC.


```bash
Tasks to be reported:

-----------------------------------------------
        date       type      summary  hours                  link_to     status
0 2020-10-20   Workshop  Hello world      2  some oppty                  Completed
1 2020-10-20  PoC / PoV     John Doe      8  another opty                Completed
-----------------------------------------------
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

That's it. Now the script will open a controlled Firefox browser and load all the tasks. Once it's done you will see the message:

```bash
Reporting done
```
