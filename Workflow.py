from main import logger
from Connection import Connection
from DriverAction import DriverAction, By
from SaveAction import SaveToolKit
from ParseToolkits import ToolKits
from abc import ABC, abstractmethod
from typing import Union, Literal, List


class Workflow(ABC):
    def __init__(self, by:By, *params:any) -> None:
        
        super().__init__()
        self.driver = Connection(*params).driver_instance()
        self.by = by
        self.driver_action = DriverAction(self.driver, self.by)

    @logger.catch
    @abstractmethod
    def driver_flow(self) -> any:
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
        output = self.driver_flow()
        parse_result = self.parse_flow(output)
        self.save_flow(parse_result)
