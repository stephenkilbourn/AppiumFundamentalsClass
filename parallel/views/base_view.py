from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BaseView(object):
  def __init__(self, driver):
    self.driver = driver
    self.wait = WebDriverWait(self.driver, 10)

  def wait_for(self, locator):
    return self.wait.until(EC.presence_of_element_located(locator))

  def find(self, locator):
    return self.driver.find_element(*locator)

  def getURL(self, url):
    self.driver.get(url)

  def terminateApp(self, appName):
    self.driver.terminate_app(appName)

  def launchSafari(self):
    self.driver.execute_script('mobile: launchApp', {'bundleId': 'com.apple.mobilesafari'})

  @classmethod
  def instance(cls, driver):
    android_cls = getattr(cls, '_ANDROID', cls)
    ios_cls = getattr(cls, '_IOS', cls)
    actual_cls = ios_cls if driver._platform == 'ios' else android_cls
    return actual_cls(driver)