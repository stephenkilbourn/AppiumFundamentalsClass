from appium.webdriver.common.mobileby import MobileBy

from views.base_view  import BaseView
from views.echo_view import EchoView
from views.login_view import LoginView

class HomeView(BaseView):

  ECHO_ITEM = (MobileBy.ACCESSIBILITY_ID, 'Echo Box')
  LOGIN_ITEM = (MobileBy.ACCESSIBILITY_ID, 'Login Screen')
  
  def nav_to_echobox(self):
      self.wait_for(self.ECHO_ITEM).click()
      return EchoView.instance(self.driver)

  def nav_to_login(self):
      self.wait_for(self.LOGIN_ITEM).click()
      return LoginView.instance(self.driver)