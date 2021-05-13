from appium.webdriver.common.mobileby import MobileBy
from views.base_view  import BaseView


class LoginView(BaseView):
  def login(self, username, password):
    from views.secret_view import SecretView
    self.wait_for(self.USERNAME_INPUT).send_keys(username)
    self.wait_for(self.PASSWORD_INPUT).send_keys(password)
    self.find(self.LOGIN_BUTTON).click()
    return SecretView.instance(self.driver)

  def loginLoaded(self):
    self.wait_for(self.USERNAME_INPUT)



class LoginViewIOS(LoginView):
  LOGIN_BUTTON = (MobileBy.XPATH, '(//XCUIElementTypeOther[@name="loginBtn"])[2]')
  PASSWORD_INPUT = (MobileBy.XPATH, '//XCUIElementTypeSecureTextField[@name="password"]')
  USERNAME_INPUT = (MobileBy.XPATH, '//XCUIElementTypeTextField[@name="username"]')

class LoginViewAndroid(LoginView):
  LOGIN_BUTTON = (MobileBy.ACCESSIBILITY_ID, 'loginBtn')
  PASSWORD_INPUT = (MobileBy.ACCESSIBILITY_ID, 'password')
  USERNAME_INPUT = (MobileBy.ACCESSIBILITY_ID, 'username')

LoginView._IOS = LoginViewIOS
LoginView._ANDROID = LoginViewAndroid