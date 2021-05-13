from appium.webdriver.common.mobileby import MobileBy
from views.base_view  import BaseView


class SecretView(BaseView):
  def getLoggedInText(self):
    return self.wait_for(self.GREETING_MESSAGE).text

  def logout(self):
    from views.login_view import LoginView
    self.wait_for(self.LOGOUT_BUTTON).click()
    return LoginView.instance(self.driver)

  def deeplink(self, username, password):
    # android
    # self.driver.execute_script('mobile:deepLink', {'url': f'theapp://login/{username}/{password}', 'package': "io.cloudgrey.the_app"})
    self.driver.execute_script('mobile: terminateApp', {'bundleId': 'com.apple.mobilesafari'})
    self.driver.execute_script('mobile: launchApp', {'bundleId': 'com.apple.mobilesafari'})
    if self.driver.is_keyboard_shown() != True:
      self.wait_for((MobileBy.XPATH, '//XCUIElementTypeButton[@name="URL"]')).click()
    self.wait_for((MobileBy.XPATH, '//XCUIElementTypeTextField[@name="URL"]')).send_keys(f'theapp://login/alice/mypassword' + '\uE007')
    self.wait_for((MobileBy.XPATH, '(//XCUIElementTypeStaticText[@name="Open"])[1]')).click()

class SecretViewIOS(SecretView):
  GREETING_MESSAGE = (MobileBy.XPATH, '///XCUIElementTypeStaticText[contains(@value,"logged in")]')
  LOGOUT_BUTTON = (MobileBy.XPATH, '(//XCUIElementTypeOther[@name="Logout"])[2]')
  OPEN_BUTTON = (MobileBy.ACCESSIBILITY_ID, 'Open')
  APP_NAME = 'io.cloudgrey.the-app'


class SecretViewAndroid(SecretView):
  GREETING_MESSAGE = (MobileBy.XPATH, '//android.widget.TextView[contains(@text,"logged in")]')
  LOGOUT_BUTTON = (MobileBy.XPATH, '//android.widget.TextView[contains(@text,"Logout")]')
  APP_NAME = 'io.cloudgrey.the_app'

SecretView._IOS = SecretViewIOS
SecretView._ANDROID = SecretViewAndroid