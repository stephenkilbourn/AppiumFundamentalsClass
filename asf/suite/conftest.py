import pytest
from appium import webdriver
from os import path

CUR_DIR = path.dirname(path.abspath(__file__))
APP = path.join(CUR_DIR, '..', 'mobile', 'TheApp.app.zip')
APPIUM = 'http://localhost:4723'


@pytest.fixture
def driver():

  CAPS = {
      'platformName': 'iOS',
      'platformVersion': '13.6',
      'deviceName': 'iPhone 11',
      'automationName': 'XCUITest',
      'app': APP,
  }

  def test_echo_box():
    driver = webdriver.Remote(
        command_executor=APPIUM,
        desired_capabilities=CAPS
        )