from main import logger
from Connection import DriverInit
from DriverAction import DriverAction, By
from abc import ABC, abstractmethod
from typing import Union, List

"""
Notice: This class is working as an experimental frame, feel free to ignore it.
"""
class Workflow(ABC):
    def __init__(self, urls: Union[str, List[str]], by:By = By.XPATH, contact:Union[dict, None] = None, 
                 email_level = "CRITICAL",*driver_params:any) -> None:
        """
        Initialize a new instance of Workflow class.
        A workflow is maded in order to perform a specific crawling task, your own implementation should inherit it.

        Parameters:
        - urls (Union[str, List[str]]): A single URL or a list of URLs to be processed by the workflow.
        - by (By, optional): The type of locator to be used for element identification. Defaults to By.XPATH.
        - contact (Union[dict, None], optional): A dictionary containing contact information for email notifications. Defaults to None.
        - email_level (str, optional): The minimum severity level for sending email notifications. Defaults to "CRITICAL".
        - *driver_params:any: Additional parameters to be passed to DriverInit class.

        Returns:
        - None
        """
        super().__init__()
        self.driver = DriverInit(*driver_params)
        self.by = by
        self.driver_action = DriverAction(self.driver, self.by, contact, email_level)
        self.urls = urls

    @logger.catch
    @abstractmethod
    def main_driver_flow(self, *mdf_input:any) -> any:
        """
        Execute the main driver flow of the workflow. Essential for running the workflow.

        Parameters:
        - *mdf_input (any): Variable length argument list for input parameters required by the driver flow.

        Returns:
        - any: The result of the driver flow execution.
        """
        return """
        complete your own driver flow
        """

    
    @logger.catch
    def parse_flow(self, *pf_input:any) -> any:
        """
        Execute the parse flow of the workflow. This function is responsible for processing
        the output from the main driver flow and preparing it for saving.

        Parameters:
        - *pf_input (any): Variable length argument list for input parameters required by the parse flow.

        Returns:
        - any: The result of the parse flow execution, which will be used in the save flow.
        """
        return """
        complete your own parse flow
        """
    
    @logger.catch
    def save_flow(self, *sf_input:any) -> None:
        """
        Execute the save flow of the workflow. This function is responsible for saving
        the processed results from the parse flow.

        Parameters:
        - *sf_input (any): Variable length argument list for input parameters required by the save flow.

        Returns:
        - None: This function does not return any value.
        """
        logger.success(f"result successfully saved")

    @logger.catch
    def run(self):
        """
        The main executing function of the crawler.
        """
        output = self.main_driver_flow()
        parse_result = self.parse_flow(output)
        self.save_flow(parse_result)
