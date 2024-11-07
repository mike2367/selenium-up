from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from typing import Union, List
from main import logger
import random
import time
class DriverAction():

    def __init__(self, driver, by: By, urls: Union[str, List[str]]) -> None:
        self.driver = driver
        self.by = by
        self.urls = urls
    @logger.catch
    def click_element(self, value:str, elementname:str, log:bool = True)-> List[str]:
        element = self.driver.find_element(self.by, value)
        element.click()
        if log:
            logger.success(f"Clicked on element {elementname}")
        return self.driver.window_handles
    
    @logger.catch
    def double_click(self, value: str, elementname: str, log:bool = True) -> List[str]:
        
        element = self.driver.find_element(self.by, value)
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        
        if log:
            logger.success(f"Doubled clicked on element {elementname}")
        return self.driver.window_handles
    @logger.catch
    def right_click(self, value: str, elementname: str, log:bool = True) -> List[str]:
        
        element = self.driver.find_element(self.by, value)
        actions = ActionChains(self.driver)
        actions.context_click(element).perform()
        
        if log:
            logger.success(f"Right clicked on element {elementname}")
        return self.driver.window_handles
    @logger.catch
    def get_element_attribute(self, value:str, attribute:str, log:bool = True)->str:
        element = self.driver.find_element(self.by, value)
        result = element.get_attribute(attribute).strip()
        if log:
            logger.success(f"Get attribute {attribute} on element, result: {result}")
        return result
    
    @logger.catch
    def input_keys(self, value:str, log:bool = True, **param:any)->None:
        element = self.driver.find_element(self.by, value)
        element.send_keys(param)
        if log:
            logger.success(f"Input text {str(param)} into element")

    @logger.catch
    def slide_horizontal(self, value: str, offset: int, log: bool = True) -> None:
        element = self.driver.find_element(self.by, value)
        actions = ActionChains(self.driver)
        actions.click_and_hold(element).move_by_offset(offset, 0).release().perform()
        if log:
            logger.success(f"Slide element by offset {offset}")
    @logger.catch
    def scroll_down(self, value:str = None, pixel:int = None, sleep_time:float = random.uniform(0.5, 1), log:bool = True)->None:
        """
        value: a By expression for element search, then driver will scroll until it is in view
        pixel: how many pixel to scroll down

        if none of the first two are provided, the page will be scrolled to the bottom gradually
        """
        if pixel:
            self.driver.execute_script('window.scrollBy(0,{})'.format(str(pixel)))
            if log:
                logger.success(f"Scroll down {pixel} pixel")
            return
        elif value:
            element = self.driver.find_element(self.by, value)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            if log:
                logger.success(f"Scroll down to element {value}")
        else:
            js = "return action=document.body.scrollHeight"
            height = 0
            new_height = self.driver.execute_script(js)
            while height < new_height:
                for i in range(height, new_height, 100):
                    self.driver.execute_script('window.scrollTo(0, {})'.format(i))
                    height = new_height
                    time.sleep(sleep_time)
                    new_height = self.driver.execute_script(js)

    @logger.catch
    def addCookies(self, cookieinstance: Union[dict, List[dict]], log: bool = True) -> None:
        if isinstance(cookieinstance, dict):
            self.driver.add_cookie(cookieinstance)
            if 'expiry' in cookie:
                del cookie['expiry']
            if log:
                logger.info(f"Added cookie: {cookieinstance}")
        elif isinstance(cookieinstance, list):
            for cookie in cookieinstance:
                self.driver.add_cookie(cookie)
                if 'expiry' in cookie:
                    del cookie['expiry']
                if log:
                    logger.info(f"Added cookie: {cookie}")
    @logger.catch
    def window_switch(self, ActionList:List[Union[int, callable]], log:bool = True)->None:
        """
        An action can be a window index or a function for taking element etc
        """
        for action in ActionList:
            if isinstance(action, int):
                self.driver.switch_to.window(action)
                if log:
                    logger.success(f"Switched to window {self.driver.title}")
            else:
                action()

    @logger.catch
    def frame_switch(self, ActionList:List[Union[str, callable]], log:bool = True)->None:
        """
        An action can be a frame name or a function for taking element etc
        """
        for action in ActionList:
            if isinstance(action, str):
                self.driver.switch_to.frame(action)
                if log:
                    logger.success(f"Switched to frame {action}")
            else:
                action()

        
