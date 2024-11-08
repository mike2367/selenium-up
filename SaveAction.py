from main import logger
from typing import List, Union
import csv


class SaveToolKit():
    
    @logger.catch
    @staticmethod
    def csv_save(filename:str, item_list:List[dict], header:list = None, encoding:str = 'utf-8')->None:
        with open(filename, 'a', newline='', encoding=encoding) as f:
            writer = csv.DictWriter(f, fieldnames=header)
            if header:
                writer.writeheader()
            writer.writerows(item_list)
        f.close()

    
    def error_rollback(func):
        def wrapper(cursor, table_name, item_list):
            try:
                func(cursor, table_name, item_list)
            except Exception as e:
                cursor.rollback()
                logger.error(f"Error inserting records into {table_name}, rollback is initiated")
                raise
        return wrapper

    @error_rollback
    @staticmethod
    def mysql_insert(cursor:any, table_name:str, item_list:List[dict])->None:
        if not item_list:
            logger.warning("item list is empty for mysql_insert, table_name: {}".format(table_name))
            return 

        columns = item_list[0].keys()
        placeholders = ', '.join(['%s'] * len(columns))
        columns_joined = ', '.join(f"`{col}`" for col in columns)
        sql = f"INSERT INTO `{table_name}` ({columns_joined}) VALUES ({placeholders})"
        values = [tuple(item[col] for col in columns) for item in item_list]
        cursor.executemany(sql, values)
        logger.success(f"Inserted {len(item_list)} records into {table_name}.")


    @logger.catch
    @staticmethod
    def mongodb_insert(collection:any, item_list: List[dict]) -> None:
        if not item_list:
            logger.warning("item list is empty for mongodb_insert.")
            return
        result = collection.insert_many(item_list)
        logger.success(f"Inserted {len(result.inserted_ids)} records into MongoDB collection.")


    @logger.catch
    @staticmethod
    def redis_insert(redis_client:any, item_list: List[dict], key_field: str, Hash:bool = True) -> None:
        if not item_list:
            logger.warning("item list is empty for redis_insert.")
            return
        for item in item_list:
            key = item.get(key_field)
            if key:
                redis_client.hset(key, mapping=item) if Hash else redis_client.set(key, item)
        logger.success(f"Inserted {len(item_list)} records into Redis.")

