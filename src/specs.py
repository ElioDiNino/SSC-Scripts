from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from setup import CWL, PASSWORD, EMAIL_LIST, CHECK_INTERVAL

# Chrome driver releases: https://chromedriver.storage.googleapis.com/index.html
s = Service('chromedriver.exe')


def specsCheck():
    found = 0

    while found == 0:

        driver = webdriver.Chrome(service=s)
        driver.get("https://cas.id.ubc.ca/ubc-cas/login?TARGET=https%3A%2F%2Fcourses.students.ubc.ca%2Fcs%2Fsecure%2Flogin%3FIMGSUBMIT.x%3D39%26IMGSUBMIT.y%3D19")

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
            search = driver.find_element(by=By.LINK_TEXT, value="Program")
            search.click()
            time.sleep(2)
        except:
            print("errorProg")

        try:
            search = driver.find_element(by=By.NAME, value="selSpec")
            search.click()
            found = 1
            sendEmail()
        except:
            print("No specializations yet")
            time.sleep(2)

        driver.quit()
        if found == 0:
            time.sleep(CHECK_INTERVAL)

    print("Specializations released!")

    return


def sendEmail():
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
            search.send_keys("Specializations Release")
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
                "Second year Engineering Specializations have been released!\n")
            search.send_keys(Keys.ENTER)
            search.send_keys(
                "Specializations are available at https://courses.students.ubc.ca/cs/courseschedule?pname=regi&tname=regi\n")
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

            time.sleep(20)

            print("Email sent!")
        except:
            print("errorSend")

    return


if __name__ == "__main__":
    specsCheck()
