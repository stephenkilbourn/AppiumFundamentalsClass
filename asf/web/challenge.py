from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

caps = {
  "headspin:capture": True,
    "headspin:initialScreenSize": {
        "width": 1920,
        "height": 1080
    },
    "browserName": "chrome",
    "browserVersion": "87.0.4280.66"
}
driver = webdriver.Remote(
    command_executor='https://dev-us-chi-0.headspin.io:9095/v0/43fd96c1797449149dab6ce9f3faf4fa/wd/hub',
    desired_capabilities=caps
)
# driver = webdriver.Firefox()

try:
  wait = WebDriverWait(driver, 10)

  driver.get('https://the-internet.herokuapp.com')

  wait.until(EC.presence_of_element_located(
    (By.LINK_TEXT, 'Add/Remove Elements')
  )).click()
  
  add_button = wait.until(EC.presence_of_element_located(
    (By.XPATH, '//button[contains(text(), "Add Element")]')
  ))

  # verify that no added elements exists
  els = driver.find_elements(By.CSS_SELECTOR, '.added-manually')
  assert len(els) == 0

# click add and verify that one element exists
  add_button.click()
  els = driver.find_elements(By.CSS_SELECTOR, '.added-manually')
  assert len(els) == 1

# click add and verify that there are now two added elements
  add_button.click()
  els = driver.find_elements(By.CSS_SELECTOR, '.added-manually')
  assert len(els) == 2

# click the first elment to delete and veriify that there are just one elements
  els[0].click()
  els = driver.find_elements(By.CSS_SELECTOR, '.added-manually')
  assert len(els) == 1
  
# click the remaining elment to delete and veriify that there are no added elements
  els[0].click()
  els = driver.find_elements(By.CSS_SELECTOR, '.added-manually')
  assert len(els) == 0

# return to the home page
  driver.back()

# go to the Dynamic Loading page 
  wait.until(EC.presence_of_element_located(
    (By.LINK_TEXT, 'Dynamic Loading')
  )).click()

# click on Example 2
  wait.until(EC.presence_of_element_located(
    (By.PARTIAL_LINK_TEXT, 'Example 2')
  )).click()

# Click the start button and wait for Hello World to load 
  wait.until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, 'button')
  )).click()
  dynamic_el =  wait.until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, '#finish')
  ))
  assert 'Hello World' in dynamic_el.text

# return to the home page
  driver.back()
  driver.back()

# go to the Frames page 
  wait.until(EC.presence_of_element_located(
    (By.LINK_TEXT, 'Frames')
  )).click()

# go to the Frames page 
  wait.until(EC.presence_of_element_located(
    (By.LINK_TEXT, 'iFrame')
  )).click()
  iFrame = wait.until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, '#mce_0_ifr')
  ))

# type in text area and verify it changes
  driver.switch_to.frame(iFrame)
  text_area = driver.find_element(By.XPATH, '//*[@id="tinymce"]')
  text_area.clear()
  text_area.send_keys('Hello from automation!')

  assert 'Hello from automation!' in text_area.text

# go back to home page
  driver.switch_to.parent_frame()
  driver.back()
  driver.back()

finally:
  driver.quit()