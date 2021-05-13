from selenium import webdriver

driver = webdriver.Firefox()
try:
  driver.get('http://the-internet.herokuapp.com')
finally:
  driver.quit()