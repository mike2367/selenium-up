from main import logger
from typing import List, Iterator
from prettytable import PrettyTable

_TABLE_COLORPLAN = {
    "title": "\033[95m",      # Magenta
    "header": "\033[33m",     # Blue
    "row": "\033[92m",        # Greenss
    "default": "\033[0m"        
}

class ParseToolKit:
    @staticmethod
    @logger.catch
    def dict_search(items: dict, key: str, log: bool = False) -> Iterator:
        """
        Searches for a specified key in a nested dictionary or list structure and yields its values.

        Args:
            items (dict): The dictionary or list to search within.
            key (str): The key to search for in the dictionary.
            log (bool): If True, logs the number of results found. Default is False.

        Yields:
            Iterator: An iterator over the values associated with the specified key.
        """
        result_num = 0
        stack = [items]
        while stack:
            current = stack.pop()
            if isinstance(current, dict):
                for k, v in current.items():
                    if k == key:
                        yield v
                        result_num += 1
                    # dict in dict
                    else:
                        stack.append(v)
            elif isinstance(current, list):
                for v in current:
                    stack.append(v)
        if log:
            logger.info("dict search completed, result_num: {result_num}")


    @staticmethod
    @logger.catch
    def spot_difference(item1, item2, title: str = "Difference Table", log: bool = False) -> dict:
        """
        Compare two JSON-like structures (dicts, lists) and output differences in table.

        Args:
            item1: First JSON-like structure (dict or list).
            item2: Second JSON-like structure (dict or list).
            title (str): Title for the difference table.
            log (bool): Whether to log the differences.

        Returns:
            dict: A dictionary containing the differences.
        """
        differences = {}

        def _compare(obj1, obj2, path=""):
            if type(obj1) != type(obj2):
                differences[path] = (obj1, obj2)
            elif isinstance(obj1, dict):
                keys1 = set(obj1.keys())
                keys2 = set(obj2.keys())
                all_keys = keys1.union(keys2)
                for key in all_keys:
                    new_path = f"{path}.{key}" if path else key
                    if key not in obj1:
                        differences[new_path] = (None, obj2[key])
                    elif key not in obj2:
                        differences[new_path] = (obj1[key], None)
                    else:
                        _compare(obj1[key], obj2[key], new_path)
            elif isinstance(obj1, list):
                len1 = len(obj1)
                len2 = len(obj2)
                min_len = min(len1, len2)
                for index in range(min_len):
                    new_path = f"{path}[{index}]"
                    _compare(obj1[index], obj2[index], new_path)
                if len1 > len2:
                    for index in range(len2, len1):
                        new_path = f"{path}[{index}]"
                        differences[new_path] = (obj1[index], None)
                elif len2 > len1:
                    for index in range(len1, len2):
                        new_path = f"{path}[{index}]"
                        differences[new_path] = (None, obj2[index])
            else:
                if obj1 != obj2:
                    differences[path] = (obj1, obj2)

        _compare(item1, item2)

        if differences:
            # Non-log version with color
            table = PrettyTable()
            if title:
                table.title = _TABLE_COLORPLAN["title"] + title + _TABLE_COLORPLAN["default"]
            table.field_names = [
                _TABLE_COLORPLAN["header"] + "Field" + _TABLE_COLORPLAN["default"],
                _TABLE_COLORPLAN["header"] + "Item1" + _TABLE_COLORPLAN["default"],
                _TABLE_COLORPLAN["header"] + "Item2" + _TABLE_COLORPLAN["default"],
            ]
            for field, (val1, val2) in differences.items():
                table.add_row([
                    _TABLE_COLORPLAN["row"] + field + _TABLE_COLORPLAN["default"],
                    _TABLE_COLORPLAN["row"] + str(val1) + _TABLE_COLORPLAN["default"],
                    _TABLE_COLORPLAN["row"] + str(val2) + _TABLE_COLORPLAN["default"],
                ])
            print(table)

            # No color version for log
            if log:
                log_table = PrettyTable()
                if title:
                    log_table.title = title
                log_table.field_names = ["Field", "Item1", "Item2"]
                for field, (val1, val2) in differences.items():
                    log_table.add_row([field, str(val1), str(val2)])
                logger.info("\nDifferences found:\n" + log_table.get_string())

        return differences

    @staticmethod
    @logger.catch
    def table_print(item_list: List[dict], title: str = "Info Table", log: bool = False) -> List[dict]:
        """
        Prints a table of items in a list of dictionaries.

        This function takes a list of dictionaries, where each dictionary represents a row in the table.
        It prints the table with optional title and logs the table to the console if the 'log' parameter is True.

        Parameters:
        - item_list (List[dict]): A list of dictionaries, where each dictionary represents a row in the table.
        - title (str): The title of the table. Default is "Info Table".
        - log (bool): A flag indicating whether to log the table to the console. Default is False.

        Returns:
        - None
        """
        if not item_list:
            logger.warning("No items to display in table.")
            return item_list
        all_keys = set()
        for item in item_list:
            all_keys.update(item.keys())
        sorted_keys = sorted(all_keys)  
        table = PrettyTable()
        if title:
            table.title = _TABLE_COLORPLAN["title"] + title + _TABLE_COLORPLAN["default"]
        table.field_names = [_TABLE_COLORPLAN["header"] + key + _TABLE_COLORPLAN["default"] for key in sorted_keys]
        for item in item_list:
            row = []
            for key in sorted_keys:
                value = item.get(key, '')  
                colored_value = f"{_TABLE_COLORPLAN['row']}{value}{_TABLE_COLORPLAN['default']}"
                row.append(colored_value)
            table.add_row(row)

        print(table)
        # No color version for log
        if log:
            log_table = PrettyTable()
            if title:
                log_table.title = title
            log_table.field_names = sorted_keys  
            for item in item_list:
                log_table.add_row([str(item.get(key, '')) for key in sorted_keys])
            logger.info("\nInfo Table Output:\n" + log_table.get_string())

        return item_list




