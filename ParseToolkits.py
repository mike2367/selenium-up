from main import logger
from typing import List, Iterator
from prettytable import PrettyTable

table_colorplan = {
    "title": "\033[95m",      # Magenta
    "header": "\033[33m",     # Blue
    "row": "\033[92m",        # Green
}
class ParseToolKits():
    @staticmethod
    def dict_search(items:dict, key: str, log:bool = False) -> Iterator:
        result_num = 0
        stack = [items]
        while stack:
            current = stack.pop()
            if isinstance(v, dict):
                for k, v in current.items():
                    if k == key:
                        yield v
                        result_num += 1
                    # dict in dict
                    else:
                        stack.append(v)
            elif isinstance(v, list):
                for v in current:
                    stack.append(v)
        if log:
            logger.info("dict search completed, result_num: {result_num}")

    @staticmethod
    def spot_difference(item1, item2, title: str = "Difference Table", log: bool = False) -> dict:
        """
        Compare two JSON-like structures (dicts, lists) and identify differences.

        Args:
            item1: First JSON-like structure (dict or list).
            item2: Second JSON-like structure (dict or list).
            title (str): Title for the difference table.
            log (bool): Whether to log the differences.

        Returns:
            dict: A dictionary containing the differences.
        """
        differences = {}

        def compare(obj1, obj2, path=""):
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
                        compare(obj1[key], obj2[key], new_path)
            elif isinstance(obj1, list):
                len1 = len(obj1)
                len2 = len(obj2)
                min_len = min(len1, len2)
                for index in range(min_len):
                    new_path = f"{path}[{index}]"
                    compare(obj1[index], obj2[index], new_path)
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

        compare(item1, item2)

        if differences:
            # Non-log version with color
            table = PrettyTable()
            if title:
                table.title = table_colorplan["title"] + title + "\033[0m"
            table.field_names = [
                table_colorplan["header"] + "Field" + "\033[0m",
                table_colorplan["header"] + "Item1" + "\033[0m",
                table_colorplan["header"] + "Item2" + "\033[0m",
            ]
            for field, (val1, val2) in differences.items():
                table.add_row([
                    table_colorplan["row"] + field + "\033[0m",
                    table_colorplan["row"] + str(val1) + "\033[0m",
                    table_colorplan["row"] + str(val2) + "\033[0m",
                ])
            print(table)

            # Log version without color
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
    def table_output(item_list: List[dict], title: str = "Info Table", log: bool = False) -> None:
        if not item_list:
            logger.warning("No items to display in table.")
            return
        table = PrettyTable()
        if title:
            table.title = table_colorplan["title"] + title + "\033[0m"
        table.field_names = [table_colorplan["header"] + key + "\033[0m" for key in item_list[0].keys()]
        for item in item_list:
            table.add_row([table_colorplan["row"] + str(value) + "\033[0m" for value in item.values()])

        print(table)
        # No color version for log
        if log:
            log_table = PrettyTable()
            if title:
                log_table.title = title
            log_table.field_names = list(item_list[0].keys())
            for item in item_list:
                log_table.add_row([str(value) for value in item.values()])
            logger.info("\nParse Table output:\n" + log_table.get_string())

            
