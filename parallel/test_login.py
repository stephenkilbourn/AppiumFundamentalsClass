username ='alice'
password = 'mypassword'

def test_login_success(home):
  login = home.nav_to_login()

  secret = login.login(username, password)
  assert username in secret.getLoggedInText()

def test_login_failure(secret):
  secret.deeplink('alice', 'mypassword')

  login = secret.logout()
  login.loginLoaded()