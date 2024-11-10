import os
from Log import Customized_Log

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

_param = {}
"""
    email contact param format:{
        "username": "you@gmail.com",
        "password": "abc123", notice this is the App password provided by IMAP service, not email password
        "to": "test@gmail.com"
    }
"""
logger = Customized_Log(contact_param=_param)




    




