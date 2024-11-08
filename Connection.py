import random
from typing import Literal, Union
from selenium import webdriver
from main import logger
import settings

standard_option: list = [
    "--user-agent={}".format(random.choice(settings.ua_list)),
    "--incognito",
    "--disable-gpu",
    "--disable-blink-features",
    "--disable-blink-features=AutomationControlled"
]

class Driver_core():
    def __init__(self, 
        selenium_driverType: Literal['Chrome', 'Firefox'] = 'Chrome',
        DriverOption_param:Union[None, list] = None,
        headless:bool = False,
        detach:bool = True         
    ) -> None:
        """
        Initialize a Connection object with the provided parameters.

        Parameters:
        url (str): The URL to connect to.
        selenium_driverType (Literal['Chrome', 'Firefox'], optional): The type of Selenium WebDriver to use. Defaults to 'Chrome'.
        DriverOption_param (Union[None, list], optional): Additional options for the WebDriver. Defaults to None.
        Headless (bool): Whether to run the WebDriver in headless mode, in here because regularly used. Defaults to False.
        Returns:
        None
        """
        self.selenium_driverType = selenium_driverType
        self.DriverOption_param = DriverOption_param
        self.headless = headless
        self.opt_params = self.DriverOption_param + standard_option if self.DriverOption_param else standard_option
        if headless:
            self.opt_params.append("--headless")
        # avoid repeated settings
        self.opt_params = list(set(self.opt_params))
        self.detach = detach
        # for fingerprint elimination
        with open('./resources/stealth.min.js', 'r') as f:
            self.js = f.read()


    def __repr__(self) -> str:
        return f"""
            WebDriver:{self.selenium_driverType}
            DriverOptions:{self.opt_params}"""

    @logger.catch
    def driver_instance(self):
        if self.selenium_driverType == 'Chrome':
            options = webdriver.ChromeOptions()
            options.binary_location = settings.CHROMIUM
            for item in self.opt_params:
                options.add_argument(item)
            options.add_experimental_option("detach", self.detach)
            driver = webdriver.Chrome(options=options)


        elif self.selenium_driverType == 'Firefox':
            options = webdriver.FirefoxOptions()
            options.binary_location = settings.FIREFOX
            for item in self.opt_params:
                options.add_argument(item)
            options.add_experimental_option("detach", self.detach)
            driver = webdriver.Firefox(options=options)
        
        if driver:
            driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': self.js})
            logger.success("Selenium driver successfully initialized")
        return driver
    
