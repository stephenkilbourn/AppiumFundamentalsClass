import math
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.webdriver.common.actions.mouse_button import MouseButton
from os import path

def get_point_on_circle(step, totalSteps, origin, radius):
    point = dict()
    theta = float(2 * math.pi * (float(step)/totalSteps))
    x = int(math.floor(math.cos(theta) * radius))
    y = int(math.floor(math.sin(theta) * radius))
    point['x'] = origin['x'] + x
    point['y'] = origin['y'] + y
    return point

def drawCircle (driver, origin, radius, steps):
    firstPoint = get_point_on_circle(0, steps, origin, radius)
    circle_draw = ActionBuilder(driver)
    finger = circle_draw.add_pointer_input(POINTER_TOUCH, 'finger')
    finger.create_pointer_move(duration=0, x=firstPoint['x'], y=firstPoint['y'])
    finger.create_pointer_down(MouseButton.LEFT)
    for i in range(1, steps + 1):
        point = get_point_on_circle(i, steps, origin, radius)
        finger.create_pointer_move(duration=100, x=point['x'], y=point['y'])
    finger.create_pointer_up(MouseButton.LEFT)
    circle_draw.perform()

def drawHorizontalLine (driver, origin, radius):
    line_draw = ActionBuilder(driver)
    finger = line_draw.add_pointer_input(POINTER_TOUCH, 'finger')
    print(f"start vline at {origin['x']-radius} and {origin['y']}")
    finger.create_pointer_move(duration=0, x=origin['x']-radius, y=origin['y'])
    finger.create_pointer_down(MouseButton.LEFT)
    print(f"end vline at {origin['x']+radius} and {origin['y']}")
    finger.create_pointer_move(duration=100, x=origin['x']+radius, y=origin['y'])
    finger.create_pointer_up(MouseButton.LEFT)
    line_draw.perform()

def drawVerticalLine (driver, origin, radius):
    line_draw = ActionBuilder(driver)
    finger = line_draw.add_pointer_input(POINTER_TOUCH, 'finger')
    print(f"end hline at {origin['x']} and {origin['y']-radius}")
    finger.create_pointer_move(duration=0, x=origin['x'], y=origin['y']-radius)
    finger.create_pointer_down(MouseButton.LEFT)
    print(f"end hline at {origin['x']} and {origin['y']+radius}")
    finger.create_pointer_move(duration=100, x=origin['x'], y=origin['y']+radius)
    finger.create_pointer_up(MouseButton.LEFT)
    line_draw.perform()


CUR_DIR = path.dirname(path.abspath(__file__))
APP = path.join(CUR_DIR, 'ApiDemos.apk')
APPIUM = 'https://jp-tyo.headspin.io:7014/v0/43fd96c1797449149dab6ce9f3faf4fa/wd/hub'

CAPS = {
    'platformName': 'Android',
    'automationName': 'UiAutomator2',
    'appPackage': 'io.appium.android.apis',
    'appActivity': '.ApiDemos',
    'deviceName': 'Pixel 3a',
    'udid': '98KAY15CRV',
    'headspin:capture': True,
}

driver = webdriver.Remote(
    command_executor=APPIUM,
    desired_capabilities=CAPS
    )
try:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'Graphics')
    )).click()
    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'AlphaBitmap')
    ))
    
    scroll = ActionBuilder(driver)
    finger = scroll.add_pointer_input(POINTER_TOUCH, 'finger')
    finger.create_pointer_move(duration=0, x=100, y=500)
    finger.create_pointer_down(MouseButton.LEFT)
    finger.create_pointer_move(duration=250, x=0, y=-500, origin="pointer")
    finger.create_pointer_up(MouseButton.LEFT)
    scroll.perform()

    driver.find_element(MobileBy.ACCESSIBILITY_ID, 'FingerPaint').click()
    wait.until(EC.presence_of_element_located(
        (MobileBy.XPATH, '//android.widget.TextView[contains(@text,"Graphics/FingerPaint")]')
    ))
    window_dimensions = driver.get_window_rect()
    print(f"window size {window_dimensions}")
    window_center = dict()
    window_center['x'] = window_dimensions.get('width')/2
    window_center['y'] = window_dimensions.get('height')/2
    radius = (window_dimensions.get('width') / 2 ) * 0.8
    print(f"window center {window_center}")
    print(f"radius {radius}")
    drawCircle (driver, window_center, radius, 40)
    drawHorizontalLine (driver, window_center, radius)
    drawVerticalLine (driver, window_center, radius)

    file_name = '/screenshot.png'

    driver.save_screenshot(CUR_DIR + file_name)


finally:
    driver.quit()
