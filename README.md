# Automatic Reporting for System Engineers (A.R.S.E.)


# Installation

## Install Python

You can check that by running a simple python -V command in your shell. The output should be something like: Python 3.8.5.

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