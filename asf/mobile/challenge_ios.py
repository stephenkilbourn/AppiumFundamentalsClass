import time
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import path

CUR_DIR = path.dirname(path.abspath(__file__))
APP = path.join(CUR_DIR, 'TheApp.app.zip')
APPIUM = 'https://dev-de-fra-0.headspin.io:7033/v0/43fd96c1797449149dab6ce9f3faf4fa/wd/hub'

CAPS = {
    'deviceName': 'iPhone 11',
    'udid': '00008030-001025121AEB802E',
    'automationName': 'XCUITest',
    'platformVersion': '13.6',
    'platformName': 'iOS',
    'bundleId': 'io.cloudgrey.the-app',
    'headspin:capture': True
}

driver = webdriver.Remote(
    command_executor=APPIUM,
    desired_capabilities=CAPS
    )
try:
    wait = WebDriverWait(driver, 10)
    # * Navigate to the Login Screen
    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'Login Screen')
    )).click()
# * Enter an incorrect username and password
    wait.until(EC.presence_of_element_located(
        (MobileBy.XPATH, '//XCUIElementTypeTextField[@name="username"]')
    )).send_keys('bad')
    driver.find_element(MobileBy.XPATH, '//XCUIElementTypeSecureTextField[@name="password"]').send_keys('bad')
    driver.find_element(MobileBy.XPATH, '(//XCUIElementTypeOther[@name="loginBtn"])[2]').click()
    
# * Assert that the alert which pops up has the text "Invalid login credentials"
    wait.until(EC.presence_of_element_located(
        (MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="Alert"]')
    ))
    driver.find_element(MobileBy.XPATH, '//XCUIElementTypeStaticText[contains(@value,"Invalid login credentials")]')


    

# * Dismiss the alert
    driver.find_element(MobileBy.ACCESSIBILITY_ID, 'OK').click()

# * Enter the correct username and password (username: alice, password: mypassword)
    login = wait.until(EC.presence_of_element_located(
        (MobileBy.XPATH, '//XCUIElementTypeTextField[@name="username"]')
    )).clear()
    login.send_keys('alice')

    driver.find_element(MobileBy.XPATH, '//XCUIElementTypeSecureTextField[@name="password"]').send_keys('mypassword')
    driver.find_element(MobileBy.XPATH, '(//XCUIElementTypeOther[@name="loginBtn"])[2]').click()
# * Assert that the resulting view mentions the user's username
    wait.until(EC.presence_of_element_located(
        (MobileBy.XPATH, '///XCUIElementTypeStaticText[contains(@value,"alice")]')
    ))
    

# * Log out
    driver.find_element(MobileBy.XPATH, '(//XCUIElementTypeOther[@name="Logout"])[2]').click()
# * Assert that the username field is now visible again
    wait.until(EC.presence_of_element_located(
        (MobileBy.XPATH, '//XCUIElementTypeTextField[@name="username"]')
    ))

finally:
    driver.quit()
