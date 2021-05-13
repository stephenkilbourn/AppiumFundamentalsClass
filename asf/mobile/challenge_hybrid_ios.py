import time
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import path

CUR_DIR = path.dirname(path.abspath(__file__))
APP = path.join(CUR_DIR, 'TheApp.app.zip')
APPIUM = 'https://dev-us-pao-0.headspin.io:7044/v0/43fd96c1797449149dab6ce9f3faf4fa/wd/hub'

CAPS = {
    'deviceName': 'iPhone 12 Mini',
    'udid': '00008101-001C54882ED0001E',
    'automationName': 'XCUITest',
    'platformVersion': '14.2',
    'platformName': 'iOS',
    'bundleId': 'io.cloudgrey.the-app',
    'headspin:capture': True
}

class webview_active(object): # wait.until(webview_active())
  def __call__(self, driver):
    for context in driver.contexts:
      if context != "NATIVE_APP":
        driver.switch_to.context(context)
        return True
    return False

driver = webdriver.Remote(
    command_executor=APPIUM,
    desired_capabilities=CAPS
    )
try:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'Webview Demo')
    )).click()
    wait.until(EC.presence_of_element_located(
        (MobileBy.XPATH, '//XCUIElementTypeTextField[@name="urlInput"]')
    )).send_keys('https://the-internet.herokuapp.com')
    driver.find_element(MobileBy.ACCESSIBILITY_ID, 'navigateBtn').click()
    wait.until(EC.presence_of_element_located(
        (MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="Alert"]')
    ))
    driver.find_element(MobileBy.XPATH, '//XCUIElementTypeButton[@name="OK"]').click()



    wait.until(webview_active())

    wait.until(EC.presence_of_element_located(
        (MobileBy.XPATH, '/html/body/center/h1')
    ))

    driver.get('https://the-internet.herokuapp.com')
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
    driver.find_element(MobileBy.XPATH, '//XCUIElementTypeOther[@name="clearBtn"]').click()

finally:
  driver.quit()
