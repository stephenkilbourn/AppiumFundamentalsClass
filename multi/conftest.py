from views.home_view import HomeView
import pytest
from appium import webdriver
from os import path

from views.home_view import HomeView


CUR_DIR = path.dirname(path.abspath(__file__))
IOS_APP = path.join(CUR_DIR, 'TheApp.app.zip')
ANDROID_APP = path.join(CUR_DIR, 'TheApp.apk')
APPIUM = 'http://localhost:4723'

IOS_CAPS = {
  'platformName': 'iOS',
  'platformVersion': '13.6',
  'deviceName': 'iPhone 11',
  'automationName': 'XCUITest',
  'app': IOS_APP ,
}

ANDROID_CAPS = {
    'platformName': 'Android',
    'deviceName': 'Android Emulator',
    'automationName': 'UiAutomator2',
    'app': ANDROID_APP,
}

def pytest_addoption(parser):
    parser.addoption('--platform', action='store', default='ios')

@pytest.fixture
def platform(request):
  plat = request.config.getoption('platform').lower()
  if plat not in ['ios', 'android']:
      raise ValueError('--platform value must be ios or android')
  return plat

@pytest.fixture
def driver(platform):
  caps = IOS_CAPS if platform == 'ios' else ANDROID_CAPS
  driver = webdriver.Remote(
      command_executor=APPIUM,
      desired_capabilities=caps
  )
  driver._platform = platform
  yield driver
  driver.quit()

@pytest.fixture
def home(driver):
  return HomeView.instance(driver)