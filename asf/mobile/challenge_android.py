from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import path

CUR_DIR = path.dirname(path.abspath(__file__))
APP = path.join(CUR_DIR, 'TheApp.apk')
APPIUM = 'https://dev-za-jhb-1.headspin.io:7016/v0/43fd96c1797449149dab6ce9f3faf4fa/wd/hub'

CAPS = {
    "deviceName": "SM-G780F",
    "udid": "RF8N93HLHZJ",
    "automationName": "UiAutomator2",
    'appPackage': 'io.cloudgrey.the_app',
    'appActivity': 'io.cloudgrey.the_app.MainActivity',
    "platformName": "Android",
    "headspin:capture": True
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
        (MobileBy.ACCESSIBILITY_ID, 'username')
    )).send_keys('bad')
    driver.find_element(MobileBy.ACCESSIBILITY_ID, 'password').send_keys('bad')
    driver.find_element(MobileBy.ACCESSIBILITY_ID, 'loginBtn').click()
    
# * Assert that the alert which pops up has the text "Invalid login credentials"
    wait.until(EC.presence_of_element_located(
        (MobileBy.ID, 'android:id/alertTitle')
    ))
    alert_text = wait.until(EC.presence_of_element_located(
        (MobileBy.ID, 'android:id/message')
    )).text

    assert "Invalid login credentials" in alert_text

# * Dismiss the alert
    driver.find_element(MobileBy.ID, 'android:id/button1').click()

# * Enter the correct username and password (username: alice, password: mypassword)
    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'username')
    )).send_keys('alice')
    driver.find_element(MobileBy.ACCESSIBILITY_ID, 'password').send_keys('mypassword')
    driver.find_element(MobileBy.ACCESSIBILITY_ID, 'loginBtn').click()
# * Assert that the resulting view mentions the user's username
    wait.until(EC.presence_of_element_located(
        (MobileBy.XPATH, '//android.widget.TextView[contains(@text,"alice")]')
    ))
    

# * Log out
    driver.find_element(MobileBy.XPATH, '//android.widget.TextView[contains(@text,"Logout")]').click()
# * Assert that the username field is now visible again
    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'username')
    ))

finally:
    driver.quit()
