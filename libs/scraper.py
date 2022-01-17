import logging
from time import sleep
from selenium.webdriver import Remote, Chrome, ChromeOptions, Safari, Firefox, Opera
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.file_detector import LocalFileDetector, UselessFileDetector

from os import getenv
from time import sleep

log = logging


def create_driver_session(session_id, executor_url, options=None):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 1, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute

    new_driver = Remote(command_executor=executor_url, desired_capabilities={}, options=options)
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute

    new_driver.file_detector = UselessFileDetector()

    return new_driver


class Scraper(object):

    def __init__(self, wait_delay=180, session_id=None, executor_url=None):
        chrome_options = ChromeOptions()
        # chrome_options.add_argument(
        #     "user-data-dir=openseachromeprofile",
        # )
        # chrome_options.page_load_strategy = 'none'
        # chrome_options.add_argument("--incognito")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option(
           "excludeSwitches", ['enable-automation']
        )

        if getenv("SCRAPE_HEADLESS", "false").lower() == "true":
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-dev-shm-usage')

        if session_id is None:
            chrome_options.binary_location = "/Applications/Opera.app/Contents/MacOS/Opera"
            self.driver = Chrome(options=chrome_options)
            # self.driver = Safari()
            # self.driver = Firefox()
        else:
            self.driver = create_driver_session(session_id, executor_url, options=chrome_options)
            print(self.driver.current_url)

        self.wait = WebDriverWait(self.driver, wait_delay)
        self.executor_url = self.driver.command_executor._url
        self.session_id = self.driver.session_id

    def close(self):
        self.driver.quit()

    def getElement(self, element):
        elementType = "id"
        elementKey = element
        if "type" in element:
            elementType = element["type"]
            elementKey = element["key"]

        if elementType == "id":
            self.wait.until(lambda cdriver: cdriver.find_element_by_id(elementKey))
            return self.driver.find_element_by_id(elementKey)
        elif elementType == "class":
            self.wait.until(lambda cdriver: cdriver.find_element_by_class_name(elementKey))
            return self.driver.find_element_by_class_name(elementKey)
        elif elementType == "name":
            self.wait.until(lambda cdriver: cdriver.find_element_by_name(elementKey))
            return self.driver.find_element_by_name(elementKey)
        elif elementType == "xpath":
            self.wait.until(lambda cdriver: cdriver.find_element_by_xpath(elementKey))
            return self.driver.find_element_by_xpath(elementKey)


    def handle(self, scrapedetails):
        last_result = None
        for instruction in scrapedetails:
            try:
                if instruction["action"] == "get":
                    last_result = self.driver.get(instruction["url"])
                elif instruction["action"] == "send_keys":
                    elem = self.getElement(instruction["element"])
                    elem.clear()
                    elem.send_keys(str(instruction["keys"]))
                elif instruction["action"] == "send_keys_direct":
                    action = (
                        ActionChains(self.driver)
                        .send_keys(str(instruction["keys"]))
                    )
                    last_result = action.perform()
                elif instruction["action"] == "send_tab":
                    action = ActionChains(self.driver).send_keys(Keys.TAB)
                    last_result = action.perform()
                elif instruction["action"] == "scroll_bottom":
                    self.driver.find_element_by_css_selector("body").send_keys(Keys.CONTROL, Keys.END)

                    # action = ActionChains(self.driver).send_keys(Keys.CONTROL, Keys.END)
                    # last_result = action.perform()
                elif instruction["action"] == "moveto":
                    last_result = self.getElement(instruction["element"])
                    action = ActionChains(self.driver)
                    action.move_to_element(last_result).perform()
                elif instruction["action"] == "click":
                    last_result = self.getElement(instruction["element"])
                    last_result.click()
                    # action = ActionChains(self.driver)
                    # action.move_to_element(last_result).click().perform()
                elif instruction["action"] == "click.perform":
                    last_result = self.getElement(instruction["element"])
                    action = ActionChains(self.driver)
                    action.move_to_element(last_result).click().perform()
                elif instruction["action"] == "wait":
                    last_result = self.getElement(instruction["element"])
                elif instruction["action"] == "waitclickable":
                    last_result = self.wait.until(element_to_be_clickable((By.ID, instruction["element"])))
                elif instruction["action"] == "waitclickable_xpath":
                    last_result = self.wait.until(element_to_be_clickable((By.XPATH, instruction["element"])))
                elif instruction["action"] == "selector":
                    last_result = Select(self.getElement(instruction["element"])).select_by_value(instruction["value"])
                elif instruction["action"] == "upload":
                    last_result = self.getElement(instruction["element"])
                    last_result.send_keys(instruction["element"]["file"])
                elif instruction["action"] == "sleep":
                    sleep(instruction.get("value", 2))
            except Exception as ex:
                log.error(instruction)
                raise ex

        return last_result

