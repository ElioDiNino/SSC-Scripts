import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import common
from setup import CWL, PASSWORD, EMAIL_LIST, EMAIL_SEND_DELAY, CHECK_INTERVAL, SEND_DATA

TARGET_URL = "https://courses.students.ubc.ca/cs/courseschedule?pname=regi&tname=regi"


def specs_check():
    common.setup()

    found = 0

    while found == 0:
        driver = common.webdriver_config(True)

        try:
            driver.get(TARGET_URL)

            WebDriverWait(driver, timeout=15).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, "#cwl > form")))
            login_button = driver.find_element(by=By.CSS_SELECTOR, value="#cwl > form")
            login_button.click()

            common.login(driver, CWL, PASSWORD)

            # Reset driver context
            driver.switch_to.default_content()

            WebDriverWait(driver, timeout=15).until(
                ec.element_to_be_clickable((By.LINK_TEXT, "Program")))

            search = driver.find_element(by=By.LINK_TEXT, value="Program")
            search.click()

            try:
                time.sleep(2)

                search = driver.find_element(by=By.NAME, value="selSpec")
                search.click()
                search = driver.find_element(
                    by=By.CLASS_NAME, value="program-spec-name")
                spec = search.text
                spec = spec[3:]
                found = 1

                logging.info("Specializations released!")
                send_email(spec)
            except:
                logging.info("No specializations yet")
                time.sleep(2)

        except Exception as e:
            logging.exception("Error Checking Specializations:")
            driver.save_screenshot("ssc_error_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".png")

        driver.quit()

        if found == 0:
            time.sleep(CHECK_INTERVAL)

    return


def send_email(spec):
    sent_email = 0

    while sent_email == 0:
        driver = common.webdriver_config(False)

        try:
            driver.get("https://webmail.student.ubc.ca/")

            common.login(driver, CWL + "@student.ubc.ca", PASSWORD)

            WebDriverWait(driver, timeout=15).until(ec.element_to_be_clickable(
                (By.XPATH, "//*[@title = 'Write a new message (N)']")))

            search = driver.find_element(
                by=By.XPATH, value="//*[@title = 'Write a new message (N)']")
            search.click()

            WebDriverWait(driver, timeout=15).until(
                ec.element_to_be_clickable((By.XPATH, "//*[@title = 'Send']")))

            search = driver.find_element(
                by=By.XPATH, value="//*[@aria-label = 'To']")
            for email in EMAIL_LIST:
                search.send_keys(email)
                search.send_keys(Keys.TAB)

            WebDriverWait(driver, timeout=15).until(
                ec.element_to_be_clickable((By.XPATH, "//*[@aria-label = 'Subject,']")))

            search = driver.find_element(
                by=By.XPATH, value="//*[@aria-label = 'Subject,']")
            search.click()
            search.send_keys("Specializations Release")

            WebDriverWait(driver, timeout=15).until(
                ec.element_to_be_clickable((By.XPATH, "//*[@aria-label = 'Message body']")))

            search = driver.find_element(
                by=By.XPATH, value="//*[@aria-label = 'Message body']")
            search.clear()
            search.send_keys("Hello,\n")
            search.send_keys(Keys.ENTER)
            search.send_keys(
                "Second year Engineering Specializations have been released!\n")
            search.send_keys(Keys.ENTER)
            if SEND_DATA:
                search.send_keys("Specialization found: " + spec + "\n")
                search.send_keys(Keys.ENTER)
            search.send_keys(
                "Specializations are available at https://courses.students.ubc.ca/cs/courseschedule?pname=regi&tname"
                "=regi\n")
            search.send_keys(Keys.ENTER)
            italic = driver.find_element(
                by=By.XPATH, value="//*[@aria-label = 'Italics']")
            italic.click()
            search.send_keys("This is an automated email")

            WebDriverWait(driver, timeout=15).until(
                ec.element_to_be_clickable((By.XPATH, "//*[@title = 'Send']")))

            search = driver.find_element(
                by=By.XPATH, value="//*[@title = 'Send']")
            search.click()
            sent_email = 1

            time.sleep(EMAIL_SEND_DELAY)

            logging.info("Email sent!")
        except Exception as e:
            logging.exception("Error sending email:")
            driver.save_screenshot("email_error_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".png")
    return


if __name__ == "__main__":
    specs_check()
