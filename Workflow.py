from main import logger
from Connection import Driver_init
from DriverAction import DriverAction, By
from abc import ABC, abstractmethod
from typing import Union, List


class Workflow(ABC):
    def __init__(self, urls: Union[str, List[str]], by:By = By.XPATH, *params:any) -> None:
        
        super().__init__()
        self.driver = Driver_init(*params).driver_instance()
        self.by = by
        self.driver_action = DriverAction(self.driver, self.by)
        self.urls = urls
    @logger.catch
    @abstractmethod
    def main_driver_flow(self) -> any:
        return """
        complete your own driver flow
        """
    
    @logger.catch
    def parse_flow(self, input:any) -> any:
        return """
        complete your own parse flow
        """
    @logger.catch
    def save_flow(self, input:any) -> None:
        logger.success(f"result successfully saved")

    @logger.catch
    def run(self):
        output = self.main_driver_flow()
        parse_result = self.parse_flow(output)
        self.save_flow(parse_result)
