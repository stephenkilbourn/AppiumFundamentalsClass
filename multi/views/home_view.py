from appium.webdriver.common.mobileby import MobileBy

from views.base_view  import BaseView
from views.echo_view import EchoView

class HomeView(BaseView):

  ECHO_ITEM = (MobileBy.ACCESSIBILITY_ID, 'Echo Box')
  
  def nav_to_echobox(self):
      self.wait_for(self.ECHO_ITEM).click()
      return EchoView.instance(self.driver)
