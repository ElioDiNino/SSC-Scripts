import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import common
from setup import CWL, PASSWORD, EMAIL_LIST, EMAIL_SEND_DELAY, CHECK_INTERVAL, SEND_DATA, courses

TARGET_URL = ("https://cas.id.ubc.ca/ubc-cas/login?TARGET=https%3A%2F%2Fssc.adm.ubc.ca%2Fsscportal%2Fservlets"
              "%2FSSCMain.jsp%3Ffunction%3DSessGradeRpt")


def grades_check(check_courses: list):
    common.setup()

    found_courses = []
    found = 0
    orig_length = len(check_courses)

    while found < orig_length:
        driver = common.webdriver_config(True)

        try:
            driver.get(
                "https://cas.id.ubc.ca/ubc-cas/login?TARGET=https%3A%2F%2Fssc.adm.ubc.ca%2Fsscportal%2Fservlets"
                "%2FSSCMain.jsp%3Ffunction%3DSessGradeRpt")

            common.login(driver, CWL, PASSWORD)

            WebDriverWait(driver, timeout=15).until(
                ec.frame_to_be_available_and_switch_to_it("iframe-main"))

            # Search through grades and find the right course(s)
            for course in check_courses:
                search = driver.find_element(
                    by=By.ID, value="allSessionsGrades")
                search = search.find_elements(
                    by=By.XPATH, value="//tbody/tr/td[1]")
                for result in search:
                    if result.text == course:
                        search = result
                        break
                parent = search.find_element(by=By.XPATH, value="..")
                grade = parent.find_element(by=By.XPATH, value="td[3]")
                # Check if there's a grade yet
                if grade.text == " " or grade.text == "":
                    logging.info("No grade for " + course + " yet")
                else:
                    logging.info("Grade for " + course + ": " + grade.text)
                    grade_value = grade.text
                    found += 1
                    send_email(course, grade_value)
                    found_courses.append(course)

            for course in found_courses:
                check_courses.remove(course)
            found_courses = []

        except Exception as e:
            logging.exception("Error Checking SSC:")
            driver.save_screenshot("ssc_error_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".png")

        driver.quit()

        if found < orig_length:
            logging.info("Delay before retrying check")
            time.sleep(CHECK_INTERVAL)

    logging.info("All grades found!")
    return


def send_email(course: str, grade_value: str):
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
            search.send_keys("Course Grade Release - " + course)

            WebDriverWait(driver, timeout=15).until(
                ec.element_to_be_clickable((By.XPATH, "//*[@aria-label = 'Message body']")))

            search = driver.find_element(
                by=By.XPATH, value="//*[@aria-label = 'Message body']")
            search.clear()
            search.send_keys("Hello,\n")
            search.send_keys(Keys.ENTER)
            search.send_keys(
                "The following course grade has been released:\n")
            search.send_keys(Keys.ENTER)
            search.send_keys(course + "\n")
            search.send_keys(Keys.ENTER)
            if SEND_DATA:
                search.send_keys("Grade found: " + grade_value + "\n")
                search.send_keys(Keys.ENTER)
            search.send_keys(
                "SSC Grades are available at https://ssc.adm.ubc.ca/sscportal/servlets/SSCMain.jsp?function"
                "=SessGradeRpt\n")
            search.send_keys(Keys.ENTER)
            search.send_keys(Keys.CONTROL + "i")
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
    grades_check(courses)
