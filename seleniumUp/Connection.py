from typing import Literal, Union
from selenium import webdriver
from .main import logger
from os import path
from .settings import CHROMIUM, FIREFOX

from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.webdriver.firefox.service import Service as FirefoxService

_STANDARD_DRIVER_OPTIONS: list = [
    "--incognito",
    "--disable-gpu",
    "--disable-blink-features=AutomationControlled"
]

"""
experimental options require being manually added to the dict and are only suitable for Chrome driver
"""
_EXPERIMENTAL_OPTIONS: dict = {
    "detach": True,
    "excludeSwitches": ['enable-automation', 'enable-logging']
}

_RETRY_CONNECT_TIMES = 3
class _DriverCore:
    def __init__(self,
                 selenium_driver_type: Literal['Chrome', 'Firefox'] = 'Chrome',
                 driver_option_param: Union[None, list] = None,
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
        
        self.selenium_driverType = selenium_driver_type
        self.DriverOption_param = driver_option_param
        self.headless = headless
        self.opt_params = self.DriverOption_param + _STANDARD_DRIVER_OPTIONS if self.DriverOption_param else _STANDARD_DRIVER_OPTIONS
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
        self.undefined_js = """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                    })
                """
        with open('../resources/stealth.min.js', 'r') as f:
            self.stealth_js = f.read()
        f.close()

    def __repr__(self) -> str:
        print("-" * 100)
        driver_info = """
            WebDriver: {}
            DriverOptions: {}""".format(self.selenium_driverType, self.opt_params)
        logger.info(f"Driver info: {driver_info}")
        return "-" * 100

   

class DriverInit(object):
    def __new__(cls, *args, **kwargs):
        instance = super(DriverInit, cls).__new__(cls)
        instance.__init__(*args, **kwargs)
        return instance._driver_instance()
    def __init__(self,
                 selenium_driver_type: Literal['Chrome', 'Firefox'] = 'Chrome',
                 driver_option_param: Union[None, list] = None,
                 headless: bool = False,
                 ) -> None:
        self._driver_core = _DriverCore(selenium_driver_type, driver_option_param, headless)
        self._selenium_driverType = self._driver_core.selenium_driverType
        self._opt_params = self._driver_core.opt_params
        self._script_func = self._driver_core.script_func
        self._CHR_mem_js = self._driver_core.CHR_mem_js
        self._stealth_js = self._driver_core.stealth_js
        self._undefined_js = self._driver_core.undefined_js


    """
    This function is explictly used for non-chrome browser to eliminate driver signiture
    and is required to be executed every time before possible validation
    """

    @staticmethod
    @logger.catch
    def insert_undefined_js(driver:any)->None:
        undefined_js = """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                    })
                """
        driver.execute_script(undefined_js)
    @logger.catch
    def _driver_instance(self):
        """
        Initializes and returns a Selenium WebDriver instance based on the specified browser type.

        This function configures the WebDriver with the specified options and experimental settings,
        and applies scripts to modify browser fingerprinting properties.

        Returns:
            WebDriver: A configured Selenium WebDriver instance for the specified browser type.
        """
        if self._selenium_driverType == 'Chrome':
            options = webdriver.ChromeOptions()
            # config your own driver loc in settings
            service = ChromeService(executable_path=path.join(CHROMIUM, "chromedriver.exe"))
            for item in self._opt_params:
                options.add_argument(item)
            for opt in _EXPERIMENTAL_OPTIONS:
                options.add_experimental_option(opt, _EXPERIMENTAL_OPTIONS[opt])
            for _ in range(_RETRY_CONNECT_TIMES):
                try:
                    driver = webdriver.Chrome(service=service, options=options)
                    break
                except:
                    pass
            if driver:
                driver.execute_cdp_cmd(self._script_func, {'source': self._stealth_js})
                driver.execute_cdp_cmd(self._script_func, {"source": self._undefined_js})
                # To deal with CHR memory fail
                driver.execute_cdp_cmd(self._script_func, {"source": self._CHR_mem_js})
                logger.success("Selenium driver successfully initialized")
                print(self._driver_core)
                return driver
                


        elif self._selenium_driverType == 'Firefox':
            options = webdriver.FirefoxOptions()
            # config your own binary loc in settings
            service = FirefoxService(executable_path=path.join(FIREFOX, "geckodriver.exe"))
            for item in self._opt_params:
                options.add_argument(item)
            for _ in range(_RETRY_CONNECT_TIMES):
                try:
                    driver = webdriver.Firefox(service=service, options=options)
                    break
                except:
                    pass
            if driver:
                logger.success("Selenium driver successfully initialized")
                print(self._driver_core)
                return driver

    

    def __repr__(self) -> str:
        return self._driver_core.__repr__()
