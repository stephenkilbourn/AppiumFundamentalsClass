from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.webdriver.common.actions.mouse_button import MouseButton
from os import path

CUR_DIR = path.dirname(path.abspath(__file__))
APPIUM = 'https://dev-za-jhb-1.headspin.io:7015/v0/43fd96c1797449149dab6ce9f3faf4fa/wd/hub'

CAPS = {
    'deviceName': 'iPhone 11',
    'udid': '00008030-001D55810CD8402E',
    'automationName': 'XCUITest',
    'platformVersion': '14.0',
    'platformName': 'iOS',
    'bundleId': 'com.apple.Maps',
    'headspin:capture': True
}

driver = webdriver.Remote(
    command_executor=APPIUM,
    desired_capabilities=CAPS
    )
try:
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'Search for a place or address')
    )).send_keys('Vancouver, BC')
    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'Vancouver, BC')
    )).click()
    stanley_location = wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'Stanley Park')
    )).location
    print(f'stanley is at {stanley_location}')

    longPress = ActionBuilder(driver)
    finger = longPress.add_pointer_input(POINTER_TOUCH, 'finger')
    finger.create_pointer_move(duration=0, x=stanley_location['x'], y=stanley_location['y'])
    finger.create_pointer_down(MouseButton.LEFT)
    finger.create_pause(2)
    finger.create_pointer_up(MouseButton.LEFT)
    longPress.perform()


    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'Preview')
    ))

    dismissPress = ActionBuilder(driver)
    finger = dismissPress.add_pointer_input(POINTER_TOUCH, 'finger')
    finger.create_pointer_move(duration=0, x=100, y=100)
    finger.create_pointer_down(MouseButton.LEFT)
    finger.create_pause(1)
    finger.create_pointer_up(MouseButton.LEFT)
    dismissPress.perform()


    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'Settings')
    ))

    # TODO fingers start plus and minus stanley x and move out
    zoomPress = ActionBuilder(driver)
    finger1 = zoomPress.add_pointer_input(POINTER_TOUCH, 'finger')
    finger1.create_pointer_move(duration=0, x=stanley_location['x']-5, y=stanley_location['y'])
    finger1.create_pointer_down(MouseButton.LEFT)
    finger1.create_pause(1)
    finger1.create_pointer_move(duration=500, x=stanley_location['x']-28, y=stanley_location['y'])
    finger1.create_pointer_up(MouseButton.LEFT)

    finger2 = zoomPress.add_pointer_input(POINTER_TOUCH, 'finger2')
    finger2.create_pointer_move(duration=0, x=stanley_location['x']+5, y=stanley_location['y'])
    finger2.create_pointer_down(MouseButton.LEFT)
    finger2.create_pause(1)
    finger2.create_pointer_move(duration=500, x=stanley_location['x']+28, y=stanley_location['y'])
    finger2.create_pointer_up(MouseButton.LEFT)
    zoomPress.perform()

    file_name = '/ios_screenshot.png'

    driver.save_screenshot(CUR_DIR + file_name)
    
finally:
    driver.quit()
