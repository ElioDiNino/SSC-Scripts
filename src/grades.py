from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from setup import CWL, PASSWORD, EMAIL_LIST, EMAIL_SEND_DELAY, CHECK_INTERVAL, SEND_DATA, courses

# Chrome driver releases: https://chromedriver.storage.googleapis.com/index.html
s = Service('chromedriver.exe')


def gradesCheck(courses: list):
    foundCourses = []
    found = 0
    origLength = len(courses)

    while found < origLength:
        try:
            options = Options()
            options.add_experimental_option(
                'excludeSwitches', ['enable-logging'])

            driver = webdriver.Chrome(service=s, options=options)
            driver.get(
                "https://cas.id.ubc.ca/ubc-cas/login?TARGET=https%3A%2F%2Fssc.adm.ubc.ca%2Fsscportal%2Fservlets%2FSSCMain.jsp%3Ffunction%3DSessGradeRpt")

            login(driver, CWL, PASSWORD)

            WebDriverWait(driver, timeout=15).until(
                EC.frame_to_be_available_and_switch_to_it("iframe-main"))

            # Search through grades and find the right course(s)
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
                # Check if there's a grade yet
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
            print("Error Checking SSC: " + str(e))

        driver.quit()

        if found < origLength:
            print("Delay before retrying check")
            time.sleep(CHECK_INTERVAL)

    print("All grades found!")
    return


def sendEmail(course: str, gradeValue: str):
    sentEmail = 0

    while sentEmail == 0:
        try:
            driver = webdriver.Chrome(service=s)
            driver.get("https://webmail.student.ubc.ca/")

            login(driver, CWL + "@student.ubc.ca", PASSWORD)

            WebDriverWait(driver, timeout=15).until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@title = 'Write a new message (N)']")))

            search = driver.find_element(
                by=By.XPATH, value="//*[@title = 'Write a new message (N)']")
            search.click()

            WebDriverWait(driver, timeout=15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@title = 'Send']")))

            search = driver.find_element(
                by=By.XPATH, value="//*[@aria-label = 'To']")
            for email in EMAIL_LIST:
                search.send_keys(email)
                search.send_keys(Keys.TAB)

            WebDriverWait(driver, timeout=15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@aria-label = 'Subject,']")))

            search = driver.find_element(
                by=By.XPATH, value="//*[@aria-label = 'Subject,']")
            search.click()
            search.send_keys("Course Grade Release - " + course)

            WebDriverWait(driver, timeout=15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@aria-label = 'Message body']")))

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

            WebDriverWait(driver, timeout=15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@title = 'Send']")))

            search = driver.find_element(
                by=By.XPATH, value="//*[@title = 'Send']")
            search.click()
            sentEmail = 1

            time.sleep(EMAIL_SEND_DELAY)

            print("Email sent!")
        except Exception as e:
            print("Error sending email: " + str(e))
    return


def login(driver: webdriver.Chrome, username: str, password: str):
    # Wait for login page to load
    time.sleep(1)
    WebDriverWait(driver, timeout=15).until(EC.visibility_of(driver.find_element(
        by=By.ID, value="username")))

    # Fill in username field
    search = driver.find_element(by=By.NAME, value="username")
    search.click()
    search.send_keys(username)

    # Fill in password field and submit login
    search = driver.find_element(by=By.NAME, value="password")
    search.send_keys(password)
    search.send_keys(Keys.RETURN)


if __name__ == "__main__":
    gradesCheck(courses)
