from main import logger
from typing import List, Iterator
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import csv


class SaveToolKit():
    
    @logger.catch
    @staticmethod
    def csv_save(filename: str, item_list: Iterator[dict], encoding: str = 'utf-8', 
                 max_workers: int = 30, log: bool = True) -> None:
        """
        Saves a list of dictionaries to a CSV file using multithreading.

        Args:
            filename (str): The name of the CSV file to save the data.
            item_list (Iterator[dict]): An iterator of dictionaries to be saved.
            encoding (str, optional): The encoding format for the CSV file. Defaults to 'utf-8'.
            max_workers (int, optional): The maximum number of threads to use. Defaults to 30.
            log (bool, optional): Whether to log the success message. Defaults to True.

        Returns:
            None
        """
        lock = Lock()

        def _single_item(item: dict, write_headers: bool = True) -> None:
            """
            Writes a single dictionary item to the CSV file.

            Args:
                item (dict): The dictionary item to write.
                write_headers (bool, optional): Whether to write headers. Defaults to True.

            Returns:
                None
            """
            header = list(item.keys())
            mode = 'w' if write_headers else 'a'
            with lock:
                with open(filename, mode, newline='', encoding=encoding) as f:
                    writer = csv.DictWriter(f, fieldnames=header)
                    if write_headers:
                        writer.writeheader()
                    writer.writerow(item)

        first = True
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for num, item in enumerate(item_list, start=1):
                executor.submit(_single_item, item, first)
                first = False
        if log:
            logger.success(f"Inserted {num} records into {filename}.")
        executor.shutdown()

    def error_rollback(func):
        """
        Decorator to handle errors and rollback transactions in case of failure.

        Args:
            func (function): The function to wrap.

        Returns:
            function: The wrapped function with error handling.
        """
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
    def mysql_insert(cursor: any, table_name: str, item_list: List[dict], log: bool = True) -> None:
        """
        Inserts a list of dictionaries into a MySQL table.

        Args:
            cursor (any): The database cursor for executing SQL commands.
            table_name (str): The name of the table to insert data into.
            item_list (List[dict]): A list of dictionaries representing the records to insert.
            log (bool, optional): Whether to log the success message. Defaults to True.

        Returns:
            None
        """
        if not item_list:
            logger.warning("item list is empty for mysql_insert, table_name: {table_name}")
            return

        columns = item_list[0].keys()
        placeholders = ', '.join(['%s'] * len(columns))
        columns_joined = ', '.join(f"`{col}`" for col in columns)
        sql = f"INSERT INTO `{table_name}` ({columns_joined}) VALUES ({placeholders})"
        values = [tuple(item[col] for col in columns) for item in item_list]
        cursor.executemany(sql, values)
        if log:
            logger.success(f"Inserted {len(item_list)} records into {table_name}.")

    @logger.catch
    @staticmethod
    def mongodb_insert(collection: any, item_list: List[dict], log: bool = True) -> None:
        """
        Inserts a list of dictionaries into a MongoDB collection.

        Args:
            collection (any): The MongoDB collection to insert data into.
            item_list (List[dict]): A list of dictionaries representing the records to insert.
            log (bool, optional): Whether to log the success message. Defaults to True.

        Returns:
            None
        """
        if not item_list:
            logger.warning("item list is empty for mongodb_insert.")
            return
        result = collection.insert_many(item_list)
        if log:
            logger.success(f"Inserted {len(result.inserted_ids)} records into MongoDB collection.")

    @logger.catch
    @staticmethod
    def redis_insert(redis_client: any, item_list: List[dict], key_field: str, 
                     Hash: bool = True, log: bool = True) -> None:
        """
        Inserts a list of dictionaries into a Redis database.

        Args:
            redis_client (any): The Redis client to use for insertion.
            item_list (List[dict]): A list of dictionaries representing the records to insert.
            key_field (str): The field to use as the key in Redis.
            Hash (bool, optional): Whether to use Redis hash for storage. Defaults to True.
            log (bool, optional): Whether to log the success message. Defaults to True.

        Returns:
            None
        """
        if not item_list:
            logger.warning("item list is empty for redis_insert.")
            return
        for item in item_list:
            key = item.get(key_field)
            if key:
                redis_client.hset(key, mapping=item) if Hash else redis_client.set(key, item)
        if log:
            logger.success(f"Inserted {len(item_list)} records into Redis.")

                # Start Generation Here


