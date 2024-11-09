from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from typing import Union, List
from main import logger
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random
import time
class DriverAction():
    """
    A class to perform various actions on web elements using Selenium WebDriver.

    Attributes:
    -----------
    _driver : WebDriver
        The Selenium WebDriver instance used to interact with the web browser.
    _by : By
        The method used to locate elements on the web page.

    Methods:
    --------
    click_element(value: str, elementname: str, log: bool = True) -> List[str]:
        Clicks on a web element and logs the action.

    double_click(value: str, elementname: str, log: bool = True) -> List[str]:
        Double-clicks on a web element and logs the action.

    right_click(value: str, elementname: str, log: bool = True) -> List[str]:
        Right-clicks on a web element and logs the action.

    get_element_attribute(value: str, attribute: str, log: bool = True) -> str:
        Retrieves the value of a specified attribute from a web element and logs the action.

    input_keys(value: str, log: bool = True, *keys: any) -> None:
        Sends keys to a web element and logs the action.

    wait_element(value: str, wait_time: int = 20, log: bool = True) -> None:
        Waits for a web element to be present on the web page and logs the action.
        
    slide_horizontal(self, value: str, offset: int, log: bool = True) -> None:
        Slides a web element horizontally by a specified offset and logs the action.
    
    scroll_down(self, value:str = None, pixel:int = None, sleep_time:float = random.uniform(0.5, 1), log:bool = True)->None:
        Scrolls the web page down and logs the action.
    """

    def __init__(self, driver, by: By) -> None:
        self._driver = driver
        self._by = by
    @logger.catch
    def click_element(self, value:str, elementname:str, log:bool = True)-> List[str]:
        element = self._driver.find_element(self._by, value)
        element.click()
        if log:
            logger.info(f"Clicked on element {elementname}")
        return self._driver.window_handles
    
    @logger.catch
    def double_click(self, value: str, elementname: str, log:bool = True) -> List[str]:
        
        element = self._driver.find_element(self._by, value)
        actions = ActionChains(self._driver)
        actions.double_click(element).perform()
        
        if log:
            logger.info(f"Doubled clicked on element {elementname}")
        return self._driver.window_handles
    @logger.catch
    def right_click(self, value: str, elementname: str, log:bool = True) -> List[str]:
        
        element = self._driver.find_element(self._by, value)
        actions = ActionChains(self._driver)
        actions.context_click(element).perform()
        
        if log:
            logger.info(f"Right clicked on element {elementname}")
        return self._driver.window_handles
    @logger.catch
    def get_element_attribute(self, value:str, attribute:str, log:bool = True)->str:
        element = self._driver.find_element(self._by, value)
        result = element.get_attribute(attribute).strip()
        if log:
            logger.info(f"Get attribute {attribute} on element, result: {result}")
        return result
    
    @logger.catch
    def input_keys(self, value:str, log:bool = True, *keys:any)->None:
        element = self._driver.find_element(self._by, value)
        element.send_keys(*keys)
        if log:
            logger.info(f"Input text {str(*keys)} into element")

    @logger.catch
    def wait_element(self, value: str, wait_time: int = 20, log: bool = True) -> any:
        element = WebDriverWait(self._driver, wait_time).until(
            EC.presence_of_element_located((self._by, value))
        )
        if log:
            logger.info(f"Wait for element {value}")
        return element

    @logger.catch
    def slide_horizontal(self, value: str, offset: int, log: bool = True) -> None:
        element = self._driver.find_element(self._by, value)
        actions = ActionChains(self._driver)
        actions.click_and_hold(element).move_by_offset(offset, 0).release().perform()
        if log:
            logger.info(f"Slide element by offset {offset}")
    @logger.catch
    def scroll_down(self, value:str = None, pixel:int = None, sleep_time:float = random.uniform(0.5, 1), log:bool = True)->None:
        """
        value: a By expression for element search, then driver will scroll until it is in view
        pixel: how many pixel to scroll down

        if none of the first two are provided, the page will be scrolled to the bottom gradually
        """
        if pixel:
            self._driver.execute_script('window.scrollBy(0,{})'.format(str(pixel)))
            if log:
                logger.info(f"Scroll down {pixel} pixel")
            return
        elif value:
            element = self._driver.find_element(self._by, value)
            self._driver.execute_script("arguments[0].scrollIntoView();", element)
            if log:
                logger.info(f"Scroll down to element {value}")
        else:
            js = "return action=document.body.scrollHeight"
            height = 0
            new_height = self._driver.execute_script(js)
            while height < new_height:
                for i in range(height, new_height, 100):
                    self._driver.execute_script('window.scrollTo(0, {})'.format(i))
                    height = new_height
                    time.sleep(sleep_time)
                    new_height = self._driver.execute_script(js)
            if log:
                logger.info(f"Scroll down to the bottom")

    @logger.catch
    def add_cookies(self, cookieinstance: Union[dict, List[dict]], log: bool = True) -> None:
        if isinstance(cookieinstance, dict):
            self._driver.add_cookie(cookieinstance)
            if 'expiry' in cookie:
                del cookie['expiry']
            if log:
                logger.info(f"Added cookie: {cookieinstance}")
        elif isinstance(cookieinstance, list):
            for cookie in cookieinstance:
                self._driver.add_cookie(cookie)
                if 'expiry' in cookie:
                    del cookie['expiry']
                if log:
                    logger.info(f"Added cookie: {cookie}")
    @logger.catch
    def window_switch(self, ActionList:List[Union[int, callable]], log:bool = True)->None:
        """
        This function works as a second layer for abstract workflow,
        packing up a chain of action in ActionList for execution.
        An action can be a window index or a function for taking element etc.
        """
        for action in ActionList:
            if isinstance(action, int):
                self._driver.switch_to.window(action)
                if log:
                    logger.info(f"Switched to window {self._driver.title}")
            else:
                action()
        if log:
            logger.info(f"window switch completed")

    @logger.catch
    def frame_switch(self, ActionList:List[Union[str, callable]], log:bool = True)->None:
        """
        This function works as a second layer for abstract workflow,
        packing up a chain of action in ActionList for execution.
        An action can be a frame name or a function for taking element etc.
        """
        for action in ActionList:
            if isinstance(action, str):
                self._driver.switch_to.frame(action)
                if log:
                    logger.info(f"Switched to frame {action}")
            else:
                action()

        if log:
            logger.info(f"frame switch completed")

    
    @staticmethod
    @logger.catch
    def driver_signiture_validate(driver):
        """
        Validates the Selenium WebDriver's signature by navigating to bot.sannysoft.com,
        which is specially made for signiture test.

        Parameters:
        -----------
        driver : WebDriver
            The Selenium WebDriver instance used to interact with the web browser.

        Returns:
        --------
        None
            Logs the result of the validation process. If all checks pass, logs a success message.
            Otherwise, logs warnings for each failed check.
        """
        base_url = "https://bot.sannysoft.com/"
        driver.get(base_url)
        all_pass = True
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fp2"]/tr[20]/td[2]')))
        tds = driver.find_elements(by=By.XPATH, value='//*[@id="fp2"]/tr/td[2]')
        for td in tds:
            if td.text != "ok":
                all_pass = False
                tr = driver.find_element(by=By.XPATH, value='//*[@id="fp2"]/tr[{}]/td[1]'.format(tds.index(td) + 1))
                logger.warning(f"Selenium driver signiture test failed in: {tr.text}, type: {td.text}")

        if all_pass:
            logger.success("Selenium driver signiture passed")
