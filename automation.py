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
from typing import List
import json
from datetime import datetime
import time
import os


class TestCase():

    _id_counter = 0

    def __init__(self, body : str = "", response : List[str] = [], passed : bool = False):
        type(self)._id_counter +=1
        self.id = self._id_counter
        self.body = body
        self.response = response
        self.passed = passed
    
    def to_dict(self):
        return {
            "id": self.id,
            "body": self.body,
            "response": self.response,
            "passed": self.passed
        }
        
    
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
    case = None
    
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_find_chat (self) -> None:
            # wait for element to be clickable
        wait = WebDriverWait(self.driver, 20)
        el = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, talk_button_xpath)))
        el.click()

        if self.case:
            # ANSI escape codes for colors
            RED = '\033[91m'
            GREEN = '\033[92m'
            END = '\033[0m'
    
            print(f"{GREEN}[INFO]{END} Performing Test ID: {self.case['id']}")
            print("ID:", self.case['id'])
            print("Question:", self.case['question'])
            self.results = self.run_case(self.case['question'])
            self.case['responses'] = self.results

            #if self.case['passed']:
            print("Passed:", GREEN + "True" + END)  # Green color for passed
            print("Responses:", self.case['responses'])

            #else:
            #    print("Passed:", RED + "False" + END)  # Red color for failed
            print("." * 80)
        else:
            assert("self.case not set")

    def run_case(self, test_case : str):
        elements = []
        wait = WebDriverWait(self.driver, 20)

        #catch errors and print, only error should be from assert
        try:

            wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.RelativeLayout[@resource-id="bot.touchkin:id/smiley_parent_container"]')))
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
            time.sleep(10)

            el9 = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Kinda like this👆")))
            el9.click()

            el10 = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Reply or say help…")))
            el10.send_keys(test_case)

            el11 = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Send")))
            el11.click()

            time.sleep(10) # Wait for messages to come in
            
            for el in self.driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, 
                                                value='new UiSelector().resourceId("bot.touchkin:id/message")'):
                try:   
                    txt = el.get_attribute('text') 
                    if(txt != self.case['question']):
                        elements.append(txt)
                except Exception as e:
                    continue               

            el = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Back")))
            el.click()

            return elements            
        except Exception as error:
            print(error)

        return elements
    


def get_test_json(filePath) -> List[TestCase]:
    with open(os.path.join(os.getcwd(), filePath), "r+") as jsonFile:
        cases = []
        try:
            cases = json.load(jsonFile)
        except Exception as error:
            print(error)
    
    return cases


def set_result_json(cases : List[TestCase]):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(os.path.join(os.getcwd(), f"results-{now}.json"), "w") as jsonFile:
        try:
            json.dump(cases, jsonFile)
        except Exception as error:
            print(error)
    
    return cases


def suit(cases : List[TestCase]):
    test_suit = unittest.TestSuite()
    for case in cases:  # Add the same test 5 times
        test = TestAppium("test_find_chat")
        test.case = case
        test_suit.addTest(test)
    return test_suit

if __name__ == '__main__':
    cases = get_test_json("testcases.json")
    runner = unittest.TextTestRunner()
    runner.run(suit(cases))
    
    for case in cases:
        print(case)