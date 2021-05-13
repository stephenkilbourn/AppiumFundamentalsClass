def test_echo_box(home):
    echo = home.nav_to_echobox()

    message = 'Hello'
    echo.save_message(message)
    assert echo.read_message()== message
    home = echo.nav_back()

    echo = home.nav_to_echobox()
    assert echo.read_message() == message

def test_saved_message_is_initially_empty(home):
    echo = home.nav_to_echobox()
    assert echo.read_message() is None