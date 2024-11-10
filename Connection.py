from typing import Literal, Union
from selenium import webdriver
from main import logger
import settings

_standard_option: list = [
    "--incognito",
    "--disable-gpu",
    "--disable-blink-features=AutomationControlled"
]

_experimental_option: dict = {
    "detach": True,
    "excludeSwitches": ['enable-automation', 'enable-logging']
}

class _Driver_core():
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
        self.opt_params = self.DriverOption_param + _standard_option if self.DriverOption_param else _standard_option
        if headless:
            self.opt_params.append("--headless")
        # avoid repeated settings
        self.opt_params = list(set(self.opt_params))

        # for fingerprint elimination
        self.script_func = 'Page.addScriptToEvaluateOnNewDocument'
        self._CHR_mem_js = """
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
        print("-" * 100)
        driver_info = """
            WebDriver:{self.selenium_driverType}
            DriverOptions:{self.opt_params}"""
        logger.info(f"Driver info: {driver_info}")
        return "-" * 100

   

class Driver_init(object):
    def __new__(cls, *args, **kwargs):
        instance = super(Driver_init, cls).__new__(cls)
        instance.__init__(*args, **kwargs)
        return instance._driver_instance()
    def __init__(self, 
        selenium_driverType: Literal['Chrome', 'Firefox'] = 'Chrome',
        DriverOption_param: Union[None, list] = None,
        headless: bool = False,    
    ) -> None:
        self._driver_core = _Driver_core(selenium_driverType, DriverOption_param, headless)
        self._selenium_driverType = self._driver_core.selenium_driverType
        self._opt_params = self._driver_core.opt_params
        self._script_func = self._driver_core.script_func
        self._CHR_mem_js = self._driver_core._CHR_mem_js
        self._stealth_js = self._driver_core.stealth_js

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
            # config your own binary loc in settings
            options.binary_location = settings.CHROMIUM
            for item in self._opt_params:
                options.add_argument(item)
            for opt in _experimental_option:
                options.add_experimental_option(opt, _experimental_option[opt])
            driver = webdriver.Chrome(options=options)


        elif self._selenium_driverType == 'Firefox':
            options = webdriver.FirefoxOptions()
            # config your own binary loc in settings
            options.binary_location = settings.FIREFOX
            for item in self._opt_params:
                options.add_argument(item)
            driver = webdriver.Firefox(options=options)

        if driver:
            driver.execute_cdp_cmd(self._script_func, {'source': self._stealth_js})
            # To deal with CHR memory fail
            driver.execute_cdp_cmd(self._script_func, {"source": self._CHR_mem_js})

            logger.success("Selenium driver successfully initialized")
            print(self._driver_core)
        return driver
    

    def __repr__(self) -> str:
        return self._driver_core.__repr__()
    

driver = Driver_init()
