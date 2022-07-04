from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from setup import CWL, PASSWORD, EMAIL_LIST, EMAIL_SEND_DELAY, CHECK_INTERVAL, SEND_DATA

# Chrome driver releases: https://chromedriver.storage.googleapis.com/index.html
s = Service('chromedriver.exe')


def gradesCheck():
    # Accepts a list with each entry as "COURSE_CODE #" E.g. "MATH 100"
    courses = ["PHIL 120", "MATH 100", "MATH 152"]
    foundCourses = []
    found = 0
    origLength = len(courses)

    while found < origLength:

        driver = webdriver.Chrome(service=s)
        driver.get("https://cas.id.ubc.ca/ubc-cas/login?TARGET=https%3A%2F%2Fssc.adm.ubc.ca%2Fsscportal%2Fservlets%2FSSCMain.jsp%3Ffunction%3DSessGradeRpt")

        try:
            search = driver.find_element(by=By.NAME, value="username")
            search.send_keys(CWL)
        except:
            print("errorName")

        try:
            search = driver.find_element(by=By.NAME, value="password")
            search.send_keys(PASSWORD)
            search.send_keys(Keys.RETURN)
            time.sleep(6)
        except:
            print("errorPass")

        try:
            driver.switch_to.frame("iframe-main")
            for course in courses:
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
                if grade.text == " " or grade.text == "":
                    print("No grade for " + course + " yet")
                else:
                    print("Grade for " + course + ": " + grade.text)
                    gradeValue = grade.text
                    found += 1
                    sendEmail(course, gradeValue)
                    foundCourses.append(course)

            for course in foundCourses:
                courses.remove(course)
            foundCourses = []

        except Exception as e:
            print("errorGrades: " + str(e))

        driver.quit()

        if found < origLength:
            time.sleep(CHECK_INTERVAL)

    print("All grades found!")
    return


def sendEmail(course, gradeValue):
    sentEmail = 0

    while sentEmail == 0:

        driver = webdriver.Chrome(service=s)
        driver.get("https://webmail.student.ubc.ca/")

        time.sleep(3)

        try:
            search = driver.find_element(by=By.NAME, value="username")
            search.click()
            search.send_keys(CWL + "@student.ubc.ca")
        except:
            print("errorEmail")

        try:
            search = driver.find_element(by=By.NAME, value="password")
            search.send_keys(PASSWORD)
            search.send_keys(Keys.RETURN)
            time.sleep(3)
        except:
            print("errorPass")

        try:
            search = driver.find_element(
                by=By.XPATH, value="//*[@title = 'Write a new message (N)']")
            search.click()
            time.sleep(2)
        except:
            print("errorNewEmail")

        try:
            search = driver.find_element(
                by=By.XPATH, value="//*[@aria-label = 'To']")
            for email in EMAIL_LIST:
                search.send_keys(email)
                search.send_keys(Keys.TAB)
            time.sleep(2)
        except:
            print("errorTo")

        try:
            search = driver.find_element(
                by=By.XPATH, value="//*[@aria-label = 'Subject,']")
            search.click()
            search.send_keys("Course Grade Release - " + course)
            time.sleep(2)
        except:
            print("errorSubject")

        try:
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
                search.send_keys("Grade found: " + gradeValue + "\n")
                search.send_keys(Keys.ENTER)
            search.send_keys(
                "SSC Grades are available at https://ssc.adm.ubc.ca/sscportal/servlets/SSCMain.jsp?function=SessGradeRpt\n")
            search.send_keys(Keys.ENTER)
            search.send_keys(Keys.CONTROL + "i")
            search.send_keys("This is an automated email")
            time.sleep(2)
        except:
            print("errorTextPaste")

        try:
            search = driver.find_element(
                by=By.XPATH, value="//*[@title = 'Send']")
            search.click()
            sentEmail = 1

            time.sleep(EMAIL_SEND_DELAY)

            print("Email sent!")
        except:
            print("errorSend")

    return


if __name__ == "__main__":
    gradesCheck()
