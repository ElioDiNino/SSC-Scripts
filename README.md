# UBC SSC Scripts
This repository is home to different scripts for checking when new information (that isn't otherwise emailed at all or in a timely fashion) becomes available on [UBC's SSC](https://ssc.adm.ubc.ca/). It uses Python and the Selenium library to check SSC and then notify the specified emails through [UBC's Webmail](https://webmail.student.ubc.ca/) of what has been released.

## Current Scripts

[`grades.py`](/src/grades.py) - For getting notified when new grades are released

[`specs.py`](/src/specs.py) - For first year engineering students to get notified when Engineering Specializations have been released

Huge thank you to [@Levivus](https://github.com/Levivus) for the his original specializations script which is what allowed me to develop both of these scripts

## Setup Instructions

1. Ensure that you have Python installed. Visit [this link](https://www.python.org/downloads/) if you need to install it.
2. Make sure you have Google Chrome installed. [Download it here](https://support.google.com/chrome/answer/95346) if it is not installed already.
3. Open Google Chrome and visit `chrome://version/` to check the browser version
4. Visit this [link](https://chromedriver.storage.googleapis.com/index.html) and find the folder with the closest version to your Google Chrome version
5. Download the appropriate zip file for your system (Windows, Mac, or Linux) and extract the contents
6. Put `chromedriver.exe` in the same folder as the the scripts (inside of [`src`](/src))
7. Make sure Selenium is installed for Python. See [this link](https://www.selenium.dev/documentation/webdriver/getting_started/install_library/) for installation instructions.
8. Open your terminal and make sure you are in the right directory ([`src`](/src)). If you are at `...\SSC-Scripts>` then run `cd src` to get to `...\SSC-Scripts\src>`
9. Run `cp setup-example.py setup.py` which will make a copy of [`setup-example.py`](/src/setup-example.py) and name it `setup.py`
10. Inside of `setup.py` configure the following:

    - Add your [CWL](https://it.ubc.ca/services/accounts-passwords/campus-wide-login-cwl) and CWL password
    - Specify which email(s) you want to be notified in `EMAIL_LIST`
    - Set the `EMAIL_SEND_DELAY`, which is how long the program will wait for the email to send before closing the browser. By default, UBC Webmail has a long delay before it sends an email so make sure this delay is long enough (60 seconds is safe).
    - Set the `CHECK_INTERVAL` you want in seconds. This is the length of time the program will wait between checks.
    - Choose whether you want `SEND_DATA` to be `True` or `False`. This will determine if the information found (specialization or grade) will be included in the email that is sent. Disable this if you are emailing multiple people and you want to keep your grades/specialization private.
    - If you are running [`grades.py`](/src/grades.py), then specify the course(s) you want to watch for new grades

## Running Instructions
```python
cd src # Only if you are not already in the src folder
python script_name.py
```

E.g. `python grades.py`
