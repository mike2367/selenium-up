import os
from Log import Customized_Log

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)
"""
    param format:{
        "username": "you@gmail.com",
        "password": "abc123", notice this is the App password provided by IMAP service, not email password
        "to": "test@gmail.com"
    }
"""
param = {}
logger_instance = Customized_Log()
logger_instance.level_setting()
logger = logger_instance.log_setting(contact_param=param)


    




