from typing import Literal, Union
from selenium import webdriver
from main import logger
import settings

standard_option: list = [
    "--incognito",
    "--disable-gpu",
    "--disable-blink-features=AutomationControlled"
]

experimental_option: dict = {
    "detach":True,
    "excludeSwitches":['enable-automation', 'enable-logging']
}

class Driver_core():
    def __init__(self, 
        selenium_driverType: Literal['Chrome', 'Firefox'] = 'Chrome',
        DriverOption_param: Union[None, list] = None,
        headless: bool = False,    
    ) -> None:
        """
        Initializes the Driver_core class with specified browser settings.

        Parameters:
        -----------
        selenium_driverType : Literal['Chrome', 'Firefox'], optional
            The type of Selenium WebDriver to use. Defaults to 'Chrome'.
        
        DriverOption_param : Union[None, list], optional
            Additional driver options to be used. Defaults to None.
        
        headless : bool, optional
            If set to True, the browser will run in headless mode. Defaults to False.

        Attributes:
        -----------
        selenium_driverType : str
            Stores the type of Selenium WebDriver.
        
        DriverOption_param : Union[None, list]
            Stores additional driver options.
        
        headless : bool
            Indicates if the browser should run in headless mode.
        
        opt_params : list
            A list of options to be used by the WebDriver, including standard options and any additional options provided.
        
        script_func : str
            The function name used for adding js scripts to evaluate on a new document.
        
        CHR_mem_js : str
            JavaScript code to modify the navigator properties for fingerprint elimination.
        
        stealth_js : str
            JavaScript code read from 'stealth.min.js' for further fingerprint elimination.
        """
        
        self.selenium_driverType = selenium_driverType
        self.DriverOption_param = DriverOption_param
        self.headless = headless
        self.opt_params = self.DriverOption_param + standard_option if self.DriverOption_param else standard_option
        if headless:
            self.opt_params.append("--headless")
        # avoid repeated settings
        self.opt_params = list(set(self.opt_params))

        # for fingerprint elimination
        self.script_func = 'Page.addScriptToEvaluateOnNewDocument'
        self.CHR_mem_js = """
           Object.defineProperty(navigator, 'deviceMemory', {
                 get: () => 8
           });
           Object.defineProperty(navigator, 'userAgent', {
             get: () => 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
           });
            """
        with open('./resources/stealth.min.js', 'r') as f:
            self.stealth_js = f.read()
        f.close()

    def __repr__(self) -> str:
        return f"""
            WebDriver:{self.selenium_driverType}
            DriverOptions:{self.opt_params}"""

    @logger.catch
    def driver_instance(self):
        """
        Initializes and returns a Selenium WebDriver instance based on the specified browser type.

        This function configures the WebDriver with the specified options and experimental settings,
        and applies scripts to modify browser fingerprinting properties.

        Returns:
            WebDriver: A configured Selenium WebDriver instance for the specified browser type.
        """
        if self.selenium_driverType == 'Chrome':
            options = webdriver.ChromeOptions()
            # config your own binary loc in settings
            options.binary_location = settings.CHROMIUM
            for item in self.opt_params:
                options.add_argument(item)
            for opt in experimental_option:
                options.add_experimental_option(opt, experimental_option[opt])
            driver = webdriver.Chrome(options=options)


        elif self.selenium_driverType == 'Firefox':
            options = webdriver.FirefoxOptions()
            # config your own binary loc in settings
            options.binary_location = settings.FIREFOX
            for item in self.opt_params:
                options.add_argument(item)
            for opt in experimental_option:
                options.add_experimental_option(opt, experimental_option[opt])
            driver = webdriver.Firefox(options=options)

        if driver:
            driver.execute_cdp_cmd(self.script_func, {'source': self.stealth_js})
            # To deal with CHR memory fail
            driver.execute_cdp_cmd(self.script_func, {
                "source": self.CHR_mem_js
                })

            logger.success("Selenium driver successfully initialized")
        return driver

    
