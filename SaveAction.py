from main import logger
from typing import List, Union
import csv
import pymysql
import pymongo
import redis


class SaveAction():
    def __init__(self) -> None:
        pass
    
    @logger.catch
    @staticmethod
    def csv_save(filename:str, item_list:List[dict], header:list = None, encoding:str = 'utf-8')->None:
        with open(filename, 'a', newline='', encoding=encoding) as f:
            writer = csv.DictWriter(f, fieldnames=header)
            if header:
                writer.writeheader()
            writer.writerows(item_list)
        f.close()

    def mysql_service(self)->None:
        pass

    def mongodb_service(self)->None:
        pass

    def redis_service(self)->None:
        pass