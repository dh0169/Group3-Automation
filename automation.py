import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
import time


class TestCase():
    def __init__(self, id : int, body : str, response : str, passed : bool):
        self.id = id
        self.body = body
        self.response = response
        self.passed = passed
        
    
capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage='bot.touchkin',
    appActivity="bot.touchkin.ui.bottombar.NavigationActivity",
    language='en',
    locale='US',
    noReset = True
)

appium_server_url = 'http://localhost:4723'

talk_button_xpath="//android.widget.LinearLayout[@content-desc=\"Talk\"]/android.widget.ImageView"


class TestAppium(unittest.TestCase):

    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_find_chat (self) -> None:
        try:
            # wait for element to be clickable
            wait = WebDriverWait(self.driver, 20)
            el = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, talk_button_xpath)))
            el.click()
            self.script_exec("Just looking to chat.")
        except Exception as error:
            print(error)

    def valchecker(val):
        return ord(val)

    def script_exec(self, input_value):
        output = []
        wait = WebDriverWait(self.driver, 20)
        try:

            wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.RelativeLayout[@resource-id="bot.touchkin:id/smiley_parent_container"]')))
            time.sleep(1)
            # Step 1 : Find the device width and height
            deviceSize = self.driver.get_window_size()
            screenWidth = deviceSize['width']
            screenHeight = deviceSize['height']
            # Step 2 : # Step 6 : Find the x,y coordinate to swipe
            # # *********** down to up ************* #
            startx = screenWidth/2
            endx = screenWidth/2
            starty = screenHeight*8/9
            endy = screenHeight/9
            self.driver.swipe(start_x=startx, start_y=starty, end_x=endx, end_y=endy, duration=100)
            time.sleep(5)

            el9 = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Kinda like this👆")))
            el9.click()

            el10 = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Reply or say help…")))
            el10.send_keys(input_value)

            el11 = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Send")))
            el11.click()

            time.sleep(1)

            elements = self.driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                            value='new UiSelector().resourceId("bot.touchkin:id/message")')

            flag = True
            for element in elements:
                if element.get_attribute('text') == input_value and flag:
                    flag = False
                elif not flag:
                    output.append(element.get_attribute('text'))
                print(element.get_attribute('text'))

            el = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Back")))
            el.click()
        except Exception as error:
            print(error)

        return output




if __name__ == '__main__':
    unittest.main()
