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
        DriverOption_param:Union[None, list] = None,
        headless:bool = False,
        detach:bool = True         
    ) -> None:
        
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
        f.close()

    def __repr__(self) -> str:
        return f"""
            WebDriver:{self.selenium_driverType}
            DriverOptions:{self.opt_params}"""

    @logger.catch
    def driver_instance(self):
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
            driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': self.js})
            # To deal with CHR memory fail
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
           Object.defineProperty(navigator, 'deviceMemory', {
                 get: () => 8
           });
           Object.defineProperty(navigator, 'userAgent', {
             get: () => 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
           });
    """
                })
            
            logger.success("Selenium driver successfully initialized")
        return driver
    
