from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from typing import Union, List, Callable
from main import logger
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException as NSE
from functools import wraps
import random
import time

def wait_element_decorator(func: Callable) -> Callable:
    """
    Decorator to wait for a web element before executing the function.

    Parameters:
    -----------
    func : Callable
        The function to be decorated.

    Returns:
    --------
    Callable
        The wrapped function with element waiting logic.
    """
    @wraps(func)
    def wrapper(self, value: str, *args, wait_time: int = 20, _decorator_log: bool = False, by: By = None, **kwargs):
        by = self._by if by is None else by
        try:
            element = WebDriverWait(self._driver, wait_time).until(
                EC.presence_of_element_located((by, value))
            )
            if not element:
                raise NSE("Input element not found, please check By and make sure it is loaded correctly")
            if _decorator_log:
                logger.debug(f"Waited for element {value}")
        except Exception as e:
            logger.error(f"Error waiting for element {value}: {e}")
            raise
        return func(self, value, *args, log=kwargs.get('log', True), by=by, **kwargs)
    return wrapper

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

    double_click(value: str, elementname: str, log: bool = True, by: By = None) -> List[str]:
        Double-clicks on a web element and logs the action.

    right_click(value: str, elementname: str, log: bool = True, by: By = None) -> List[str]:
        Right-clicks on a web element and logs the action.

    get_element_attribute(value: str, attribute: str, log: bool = True, by: By = None) -> str:
        Retrieves the value of a specified attribute from a web element and logs the action.

    input_keys(value: str, log: bool = True, *keys: any, by: By = None) -> None:
        Sends keys to a web element and logs the action.

    wait_element(value: str, wait_time: int = 20, log: bool = True, by: By = None) -> None:
        Waits for a web element to be present on the web page and logs the action.
        
    slide_horizontal(self, value: str, offset: int, log: bool = True, by: By = None, slowly:bool = True) -> None:
        Slides a web element horizontally by a specified offset and logs the action.
    
    scroll_down(self, value:str = None, pixel:int = None, sleep_time:float = random.uniform(0.5, 1), log:bool = True, by: By = None)->None:
        Scrolls the web page down and logs the action.
    """

    def __init__(self, driver, by: By) -> None:
        self._driver = driver
        self._by = by
    

    @wait_element_decorator
    @logger.catch
    def click_element(self, value:str, elementname:str, log:bool = True, by: By = None) -> List[str]:
        by = self._by if by is None else by
        element = self._driver.find_element(by, value)
        element.click()
        if log:
            logger.debug(f"Clicked on element {elementname}")
        return self._driver.window_handles
    
    @wait_element_decorator
    @logger.catch
    def double_click(self, value: str, elementname: str, log:bool = True, by: By = None) -> List[str]:
        by = self._by if by is None else by
        element = self._driver.find_element(by, value)
        actions = ActionChains(self._driver)
        actions.double_click(element).perform()
        
        if log:
            logger.debug(f"Doubled clicked on element {elementname}")
        return self._driver.window_handles

    @wait_element_decorator
    @logger.catch
    def right_click(self, value: str, elementname: str, log:bool = True, by: By = None) -> List[str]:
        by = self._by if by is None else by
        element = self._driver.find_element(by, value)
        actions = ActionChains(self._driver)
        actions.context_click(element).perform()
        
        if log:
            logger.debug(f"Right clicked on element {elementname}")
        return self._driver.window_handles

    @wait_element_decorator
    @logger.catch
    def get_element_attribute(self, value:str, attribute:str, log:bool = True, by: By = None) -> str:
        by = self._by if by is None else by
        element = self._driver.find_element(by, value)
        result = element.get_attribute(attribute).strip()
        if log:
            logger.debug(f"Get attribute {attribute} on element, result: {result}")
        return result
    
    @wait_element_decorator
    @logger.catch
    def input_keys(self, value:str, *keys:any, log:bool = True, by: By = None) -> None:
        by = self._by if by is None else by
        element = self._driver.find_element(by, value)
        element.send_keys(*keys)
        if log:
            logger.debug(f"Input text {str(*keys)} into element{value}")

    @logger.catch
    def wait_element(self, value: str, wait_time: int = 20, log: bool = False, by: By = None) -> any:
        by = self._by if by is None else by
        element = WebDriverWait(self._driver, wait_time).until(
            EC.presence_of_element_located((by, value))
        )
        if not element:
            raise NSE("Input element not found, please check By and make sure it is loaded correctly")
        if log:
            logger.debug(f"Wait for element {value}")
        return element

    @wait_element_decorator
    @logger.catch
    def slide_horizontal(self, value: str, offset: int, log: bool = True, by: By = None, slowly: bool = True, slow_step:int = 10, slow_wait:float = 0.01) -> None:
        by = self._by if by is None else by
        element = self._driver.find_element(by, value)
        actions = ActionChains(self._driver)
        if not slowly:
            actions.click_and_hold(element).move_by_offset(offset, 0).release().perform()
        else:
            # move slowly
            actions.click_and_hold(element)
            i = 0
            step = slow_step 
            while i < offset:
                time.sleep(slow_wait)
                move_step = step if (offset - i) >= step else (offset - i)
                actions.move_by_offset(move_step, 0).perform()
                i += move_step
            actions.release().perform() 

        if log:
            logger.debug(f"Slide element {value} by offset {offset}")


    @logger.catch
    def scroll_down(self, value:str = None, pixel:int = None, sleep_time:float = random.uniform(0.5, 1), log:bool = True, by: By = None, slowly: bool = True, slow_step:int = 100) -> None:
        """
        value: a By expression for element search, then driver will scroll until it is in view
        pixel: how many pixel to scroll down

        if none of the first two are provided, the page will be scrolled to the bottom gradually
        """
        by = self._by if by is None else by
        if pixel:
            """
            this option is rarely used and required to wait until the loading finishes
            """
            time.sleep(sleep_time * 4) # not optimal, change on condition
            if slowly:
                    for i in range(0, pixel, slow_step):
                        scroll_amount = slow_step if (pixel - i) >= slow_step else pixel - i
                        self._driver.execute_script('window.scrollBy(0, {})'.format(str(scroll_amount)))
                        time.sleep(sleep_time)
            else:
                self._driver.execute_script('window.scrollBy(0, {})'.format(str(pixel)))
            if log:
                logger.debug(f"Scroll down {pixel} pixel")

        elif value:
            self.wait_element(value, by=by)
            element = self._driver.find_element(by, value)

            if slowly:
                current_position = self._driver.execute_script("return window.pageYOffset;")
                target_position = element.location['y']
                # 200 works as a buffer
                target = target_position - 200 if target_position > 200 else 0  

                while current_position < target:
                    current_position += slow_step
                    if current_position > target:
                        current_position = target
                    self._driver.execute_script(f"window.scrollTo(0, {current_position});")
                    time.sleep(sleep_time)
            else:
                self._driver.execute_script("arguments[0].scrollIntoView();", element)

            if log:
                logger.debug(f"Scroll down to element {value}")
        else:
            if slowly:
                js = "return action=document.body.scrollHeight"
                height = 0
                new_height = self._driver.execute_script(js)
                while height < new_height:
                    for i in range(height, new_height, slow_step):
                        self._driver.execute_script('window.scrollTo(0, {})'.format(i))
                        time.sleep(sleep_time)
                    height = new_height
                    new_height = self._driver.execute_script(js)
            else:
                """
                This action is easily detected by the website and must wait until the scroll bar is loaded, 
                thus not recommended.
                """
                time.sleep(sleep_time * 4) # not optimal, change on condition
                self._driver.execute_script("var q=document.documentElement.scrollTop=10000")

            if log:

                logger.debug(f"Scroll down to the bottom")

    """
    awaiting test
    """
    @logger.catch
    def add_cookies(self, cookieinstance: Union[dict, List[dict]], log: bool = True) -> None:
        if isinstance(cookieinstance, dict):
            self._driver.add_cookie(cookieinstance)
            if 'expiry' in cookieinstance:
                del cookieinstance['expiry']
            if log:
                logger.debug(f"Added cookie: {cookieinstance}")
        elif isinstance(cookieinstance, list):
            for cookie in cookieinstance:
                self._driver.add_cookie(cookie)
                if 'expiry' in cookie:
                    del cookie['expiry']
                if log:
                    logger.debug(f"Added cookie: {cookie}")
    
    """
    awaiting test
    """
    @logger.catch
    def window_switch(self, ActionList: List[Union[int, tuple]], log: bool = True, by: By = None) -> None:
        """
        This function works as a second layer for abstract workflow,
        packing up a chain of action in ActionList for execution.
        An action can be a window index or a function for taking element etc.
        """
        by = self._by if by is None else by
        for action in ActionList:
            if isinstance(action, int):
                self._driver.switch_to.window(action)
                if log:
                    logger.debug(f"Switched to window {self._driver.title}")
            elif isinstance(action, tuple):
                func, args, kwargs = action
                func(*args, **kwargs)
            else:
                raise ValueError("ActionList items must be either int or tuple(func, args, kwargs)")
        if log:
            logger.debug("Window switch completed")

    @logger.catch
    def frame_switch(self, ActionList: List[Union[str, tuple]], log: bool = True, by: By = None) -> None:
        """
        This function works as a second layer for abstract workflow,
        packing up a chain of actions in ActionList for execution.
        An action can be a frame locator or a tuple containing a function and its arguments.
        """
        by = self._by if by is None else by
        for action in ActionList:
            if isinstance(action, str):
                self.wait_element(action, by=by)
                element = self._driver.find_element(by, action)
                self._driver.switch_to.frame(element)
                if log:
                    logger.debug(f"Switched to frame {action}")
            elif isinstance(action, tuple):
                func, args= action
                func(*args)
            else:
                raise ValueError("ActionList items must be either str or tuple(func, args, kwargs)")
        if log:
            logger.debug("Frame switch completed")

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


