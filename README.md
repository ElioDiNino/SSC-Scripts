# UBC SSC Scripts
This repository is home to different scripts for checking when new information (that isn't otherwise emailed at all or in a timely fashion) becomes available on [UBC's SSC](https://ssc.adm.ubc.ca/).

## Current Scripts

[`grades.py`](/src/grades.py) - For getting notified when new grades are released

[`specs.py`](/src/specs.py) - For first year engineering students to get notified when Engineering Specializations have been released

Huge thank you to [@Levivus](https://github.com/Levivus) for the specializations script which is what I based my grades script off of

## Setup Instructions

1. Make sure you have Google Chrome installed. [Download it here](https://support.google.com/chrome/answer/95346) if it is not installed already.
2. Open Google Chrome and visit `chrome://version/` to check the browser version
3. Visit this [link](https://chromedriver.storage.googleapis.com/index.html) and find the folder with the closest version to your Google Chrome version
4. Download the appropriate zip file for your system and extract the contents
5. Put `chromedriver.exe` in the same folder as the the scripts (inside of [`src`](/src))
6. Make sure Selenium is installed for python. See [this link](https://selenium-python.readthedocs.io/installation.html) for installation instructions.
7. Rename [`setup-example.py`](/src/setup-example.py) to `setup.py`
8. Add your CWL and CWL password in [`setup.py`](/src/setup-example.py)
9. Specify which email(s) you want to be notified in [`setup.py`](/src/setup-example.py)
10. Set the checking interval you want in seconds in [`setup.py`](/src/setup-example.py)
11. If you are running [`grades.py`](/src/grades.py), then specify the course(s) you want to watch for grade posting

## Running Instructions
```python
cd src
python script_name.py
```

E.g. `python grades.py`
