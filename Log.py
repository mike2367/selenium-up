from loguru import logger
import yagmail
import sys
from typing import Union

class CustomLog(object):
    def __new__(cls, *args, **kwargs):
        instance = super(CustomLog, cls).__new__(cls)
        instance.__init__(*args, **kwargs)
        return instance.custom_logger
    def __init__(self, filepath: str = "./Log.log",
                     rotation: str = "00:00",
                     level: str = "DEBUG",
                     log_format: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
                     contact_param: Union[dict, None] = None,
                     new_terminal_level: str = "ERROR"
                     ) -> None:
        """
        Initialize the Customized_Log class and set up the logger.

            Args:
                filepath (str): The log file path. Defaults to "./Log.log".
                rotation (str): The log file rotation time. Defaults to "00:00".
                level (str): The log level. Defaults to "DEBUG".
                log_format (str): The log format string. Defaults to "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}".
                contact_param (Union[dict, None], optional): Parameters for email notifications. Defaults to None.
        """
        self.custom_logger = logger
        self.custom_logger.add(filepath, rotation=rotation, level=level, format=log_format)
        self._email_setting(param=contact_param)
        self._set_new_terminal_level(new_terminal_level)

    def _email_setting(self, level:str = "CRITICAL", param:Union[dict, None] = None) -> None:
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
    @staticmethod
    def contact_setting(custom_logger:any, email_level: str = "CRITICAL", param:Union[dict, None] = None) -> None:
        """
        public API for email reciever setting
        """
        if param:
            try:
                yag = yagmail.SMTP(user=param['username'], password=param['password'])
                def send_email(message):
                    yag.send(
                        to=param['to'],
                        subject='Log {} Notification'.format(email_level),
                        contents=message
                    )
                
                # Add the email sending function as a loguru handler
                custom_logger.add(send_email, level=email_level)
            except Exception as e:
                custom_logger.error(f"Failed to set up email handler: {e}")

    def _set_new_terminal_level(self, level:str="ERROR") -> None:
        """
        Add a new terminal for higher level log processing
        """
        self.custom_logger.add(sys.stdout, level=level)

    