import glob
import logging
import os
import pathlib
import shutil
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from setup import CWL, PASSWORD

FIVE_MINUTES = 5 * 60

# See README for chromedriver releases link
s = None
# Logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s   %(levelname)-5s  %(message)s',
                    datefmt='%Y-%m-%d %I:%M %p')


def login(driver: webdriver.Chrome, username: str, password: str, interactive_login: bool = False):
    # Wait for login page to load
    time.sleep(1)
    WebDriverWait(driver, timeout=15).until(ec.visibility_of(driver.find_element(
        by=By.ID, value="username")))

    # Fill in username field
    search = driver.find_element(by=By.NAME, value="username")
    search.click()
    search.send_keys(username)

    # Fill in password field and submit login
    search = driver.find_element(by=By.NAME, value="password")
    search.send_keys(password)
    search.send_keys(Keys.RETURN)

    multi_factor_auth = False

    # See if MFA login is required
    try:
        WebDriverWait(driver, timeout=10).until(
            ec.frame_to_be_available_and_switch_to_it("duo_iframe"))
        multi_factor_auth = True
        url = driver.current_url

    except:
        logging.debug("MFA login not required")

    if multi_factor_auth and interactive_login:
        logging.info("Waiting for manual MFA authentication...")
        url = driver.current_url

        WebDriverWait(driver, timeout=FIVE_MINUTES).until(
            ec.url_changes(url))

        logging.info("MFA authentication successful")

    elif multi_factor_auth:
        try:
            WebDriverWait(driver, timeout=10).until(
                ec.url_changes(url))
            logging.info("MFA authentication successful")

        except:
            logging.error("MFA login required, please restart the program to refresh the cookies. Remember to select "
                          "the \"Remember me for 30 days\" option when prompted for MFA.")


def initial_login():
    # Login to SSC manually and store the cookies to avoid having to go through MFA every time

    # Chrome options: https://www.selenium.dev/documentation/webdriver/browsers/chrome/
    options = Options()
    script_directory = pathlib.Path().absolute()
    options.add_argument(f"user-data-dir={script_directory}\\selenium")
    options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=s, options=options)
    driver.get("https://cas.id.ubc.ca/ubc-cas/login?TARGET=https%3A%2F%2Fssc.adm.ubc.ca%2Fsscportal%2Fservlets"
               "%2FSRVSSCFramework")

    login(driver, CWL, PASSWORD, True)

    driver.quit()


def find_chromedriver():
    """
    Finds the chromedriver in the current working directory

    Required since the executable will be slightly different for different platforms
    """
    global s

    # Use a wildcard search to allow for any ending/extension
    files = glob.glob('./chromedriver*')
    if len(files) == 0:
        logging.error("No chromedriver found")
        exit(1)
    s = Service(executable_path=files[0])


def setup():
    find_chromedriver()

    # Delete the selenium folder to force a new login
    script_directory = pathlib.Path().absolute()
    if os.path.exists(f"{script_directory}\\selenium"):
        shutil.rmtree(f"{script_directory}\\selenium", ignore_errors=False, onerror=None)

    initial_login()


def webdriver_config(save_data: bool) -> webdriver.Chrome:
    # Chrome options: https://www.selenium.dev/documentation/webdriver/browsers/chrome/
    options = Options()
    if save_data:
        script_directory = pathlib.Path().absolute()
        options.add_argument(f"user-data-dir={script_directory}\\selenium")
    options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])

    return webdriver.Chrome(service=s, options=options)
