from views.secret_view import SecretView
from views.home_view import HomeView
import pytest
from appium import webdriver
from os import path

from views.home_view import HomeView


CUR_DIR = path.dirname(path.abspath(__file__))
IOS_APP = path.join(CUR_DIR, 'TheApp.app.zip')
ANDROID_APP = path.join(CUR_DIR, 'TheApp.apk')
APPIUMS= ['https://dev-us-pao-0.headspin.io:7044/v0/43fd96c1797449149dab6ce9f3faf4fa/wd/hub',
 'https://dev-us-pao-0.headspin.io:7044/v0/43fd96c1797449149dab6ce9f3faf4fa/wd/hub']

IOS_CAPS = [{
    'deviceName': 'iPhone 12 Mini',
    'udid': '00008101-001C54882ED0001E',
    'automationName': 'XCUITest',
    'platformVersion': '14.2',
    'platformName': 'iOS',
    'bundleId': 'io.cloudgrey.the-app',
    'headspin:capture': True
}, 
{
    'deviceName': 'iPhone 12 Pro Max',
    'udid': '00008101-000A6D3C1AA0001E',
    'automationName': 'XCUITest',
    'platformVersion': '14.2',
    'platformName': 'iOS',
    'bundleId': 'io.cloudgrey.the-app',
    'headspin:capture': True
}]
ANDROID_CAPS = [{
    'platformName': 'Android',
    'deviceName': 'Android Emulator',
    'automationName': 'UiAutomator2',
    'app': ANDROID_APP,
}]

def pytest_addoption(parser):
    parser.addoption('--platform', action='store', default='ios')

@pytest.fixture
def worker_num(worker_id):
    if worker_id == 'master':
        worker_id = 'gw0'
    return int(worker_id[2:])

@pytest.fixture
def server(worker_num):
  if worker_num >= len(APPIUMS):
    raise Exception('Too many workers for the number of Appium servers')
  return APPIUMS[worker_num]

@pytest.fixture
def caps(platform, worker_num):
    cap_set = IOS_CAPS if platform == 'ios' else ANDROID_CAPS
    if worker_num >= len(cap_set):
        raise Exception('Too many workers for the number of capability options.')
    return cap_set[worker_num]

@pytest.fixture
def platform(request):
  plat = request.config.getoption('platform').lower()
  if plat not in ['ios', 'android']:
      raise ValueError('--platform value must be ios or android')
  return plat

@pytest.fixture
def driver(server, caps, platform):
  driver = webdriver.Remote(
      command_executor=server,
      desired_capabilities=caps
  )
  driver._platform = platform
  yield driver
  driver.quit()

@pytest.fixture
def home(driver):
  return HomeView.instance(driver)

@pytest.fixture
def secret(driver):
  return SecretView.instance(driver)