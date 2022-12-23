from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from setup import CWL, PASSWORD, EMAIL_LIST, EMAIL_SEND_DELAY, CHECK_INTERVAL, SEND_DATA
from grades import login

# Chrome driver releases: https://chromedriver.storage.googleapis.com/index.html
s = Service('chromedriver.exe')


def specsCheck():
    found = 0

    while found == 0:
        try:
            options = Options()
            options.add_experimental_option(
                'excludeSwitches', ['enable-logging'])

            driver = webdriver.Chrome(service=s, options=options)
            driver.get("https://cas.id.ubc.ca/ubc-cas/login?TARGET=https%3A%2F%2Fcourses.students.ubc.ca%2Fcs%2Fsecure%2Flogin%3FIMGSUBMIT.x%3D39%26IMGSUBMIT.y%3D19")

            login(driver, CWL, PASSWORD)

            WebDriverWait(driver, timeout=15).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Program")))

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
                sendEmail(spec)
            except:
                print("No specializations yet")
                time.sleep(2)

        except Exception as e:
            print("Error Checking Specializations: " + str(e))

        driver.quit()

        if found == 0:
            time.sleep(CHECK_INTERVAL)

    print("Specializations released!")

    return


def sendEmail(spec):
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
            search.send_keys("Specializations Release")

            WebDriverWait(driver, timeout=15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@aria-label = 'Message body']")))

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
                "Specializations are available at https://courses.students.ubc.ca/cs/courseschedule?pname=regi&tname=regi\n")
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


if __name__ == "__main__":
    specsCheck()
