import time
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import path

CUR_DIR = path.dirname(path.abspath(__file__))
APP = path.join(CUR_DIR, 'TheApp.apk')
APPIUM = 'https://dev-us-pao-0.headspin.io:7045/v0/43fd96c1797449149dab6ce9f3faf4fa/wd/hub'

CAPS = {
    'platformName': 'Android',
    'automationName': 'UiAutomator2',
    'appPackage': 'io.cloudgrey.the_app',
    'appActivity': 'io.cloudgrey.the_app.MainActivity',
    'deviceName': 'SM-G970U',
    'udid': 'R38N1062G9D',
    'headspin:capture': True,
    'headspin:autoDownloadChromedriver': True,
}


# APPIUM = 'http://localhost:4723'

# CAPS = {
#     'platformName': 'Android',
#     'deviceName': 'Android Emulator',
#     'automationName': 'UiAutomator2',
#     'app': APP,
# }

driver = webdriver.Remote(
    command_executor=APPIUM,
    desired_capabilities=CAPS
    )

class webview_active(object): # wait.until(webview_active())
  def __call__(self, driver):
    for context in driver.contexts:
      if context != "NATIVE_APP":
        driver.switch_to.context(context)
        return True
    return False

try:
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'Webview Demo')
    )).click()
    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'urlInput')
    )).send_keys('http://the-internet.herokuapp.com')
    driver.find_element(MobileBy.ACCESSIBILITY_ID, 'navigateBtn').click()
    wait.until(EC.presence_of_element_located(
        (MobileBy.ID, 'android:id/alertTitle')
    ))
    driver.find_element(MobileBy.ID, 'android:id/button1').click()


    print(driver.contexts)
    wait.until(webview_active())

    wait.until(EC.presence_of_element_located(
        (MobileBy.XPATH, '/html/body/center/h1')
    )).click()
    print(driver.context)

    driver.get('http://the-internet.herokuapp.com')
    form_auth_link = wait.until(EC.presence_of_element_located(
        (By.LINK_TEXT, 'Form Authentication')
    ))
    form_auth_link.click()
    
    username = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#username')
    ))
    username.send_keys('tomsmith')

    password = driver.find_element(By.CSS_SELECTOR, '#password')
    password. send_keys('SuperSecretPassword!')

    driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()

    wait.until(EC.presence_of_element_located(
        (By.LINK_TEXT, 'Logout')
    )).click()
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#username')
    ))
    logout_text = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#flash')
    )).text
    assert 'logged out' in logout_text
    driver.switch_to.context('NATIVE_APP')
    driver.find_element(MobileBy.ACCESSIBILITY_ID, 'clearBtn').click()

finally:
  driver.quit()
