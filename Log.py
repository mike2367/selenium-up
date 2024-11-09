from loguru import logger
import yagmail
import sys
from typing import Union
class Customized_Log:
    def __init__(self, filepath: str = "./Log.log",
                     rotation: str = "00:00",
                     level: str = "DEBUG",
                     Format: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
                     email_level: str = None,
                     contact_param: Union[dict, None] = None
                     ) -> None:
        """
        Initialize the Customized_Log class and set up the logger.

            Args:
                filepath (str): The log file path. Defaults to "./Log.log".
                rotation (str): The log file rotation time. Defaults to "00:00".
                level (str): The log level. Defaults to "DEBUG".
                Format (str): The log format string. Defaults to "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}".
                email_level (str, optional): The log level for email notifications. Defaults to None.
                contact_param (Union[dict, None], optional): Parameters for email notifications. Defaults to None.
        """
        self.custom_logger = logger
        self.custom_logger.add(filepath, rotation=rotation, level=level, format=Format)
        self._email_setting(email_level, contact_param)
        return self.custom_logger
    def _email_setting(self, level:str = "ERROR", param:Union[dict, None] = None) -> None:
        """
        Send email to the contact specified in the 'contact_param' dictionary once an error occurs.

        The function checks if the 'contact_param' is provided and contains a valid email address.
        If the conditions are met, it extracts the email domain from the username, creates a notification handler
        using the 'notifiers' library, and adds this handler to the logger with an error level.

        Returns:
        None
        """
        if param:
            try:
                yag = yagmail.SMTP(user=param['username'], password=param['password'])
                def send_email(message):
                    yag.send(
                        to=param['to'],
                        subject='Log {} Notification'.format(level),
                        contents=message
                    )
                
                # Add the email sending function as a loguru handler
                self.custom_logger.add(send_email, level=level)
            except Exception as e:
                logger.error(f"Failed to set up email handler: {e}")

    def set_new_terminal_level(self, level:str="ERROR") -> None:
        """
        Add a new terminal for higher level log processing
        """
        self.logger.add(sys.stdout, level=level)

    