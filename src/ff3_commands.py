# This mess has been created by GearsOfLaw https://github.com/gearsoflaw
""" All commands available to be used in FF3 """
import time
from directkeys import PressKey, ReleaseKey, Keys

KEY_PRESS_DURATION = 0.09

class FF3Commands:
    """ All commands available to be used in FF3 """

    @staticmethod
    def hold_up():
        """ Hold Up/Forward button """
        PressKey(Keys.W)

    @staticmethod
    def hold_down():
        """ Hold Down/Backward button """
        PressKey(Keys.S)

    @staticmethod
    def hold_left():
        """ Hold Left button pressed """
        PressKey(Keys.A)

    @staticmethod
    def hold_right():
        """ Hold Right button pressed """
        PressKey(Keys.D)

    @staticmethod
    def quick_action():
        """ Action button pressed and released """
        PressKey(Keys.Enter)
        time.sleep(KEY_PRESS_DURATION)
        ReleaseKey(Keys.Enter)

    @staticmethod
    def quick_cancel():
        """ Cancel button pressed and released """
        PressKey(Keys.Backspace)
        time.sleep(KEY_PRESS_DURATION)
        ReleaseKey(Keys.Backspace)

    @staticmethod
    def quick_up():
        """ Up/Forward button pressed and released """
        PressKey(Keys.W)
        time.sleep(KEY_PRESS_DURATION)
        ReleaseKey(Keys.W)
        time.sleep(KEY_PRESS_DURATION)

    @staticmethod
    def quick_down():
        """ Down/Backward button pressed and released """
        PressKey(Keys.S)
        time.sleep(KEY_PRESS_DURATION)
        ReleaseKey(Keys.S)
        time.sleep(KEY_PRESS_DURATION)

    @staticmethod
    def quick_left():
        """ Left button pressed and released """
        PressKey(Keys.A)
        time.sleep(KEY_PRESS_DURATION)
        ReleaseKey(Keys.A)

    @staticmethod
    def quick_right():
        """ Right button pressed and released """
        PressKey(Keys.D)
        time.sleep(KEY_PRESS_DURATION)
        ReleaseKey(Keys.D)

    @staticmethod
    def release_all():
        """ Releases all known command buttons """
        ReleaseKey(Keys.W)
        ReleaseKey(Keys.A)
        ReleaseKey(Keys.S)
        ReleaseKey(Keys.D)
        ReleaseKey(Keys.Backspace)
        ReleaseKey(Keys.Enter)
