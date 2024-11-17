## File Contents
### Log.py
- Defines `CustomLog`, which wraps library `loguru` and `yagmail`.
- ### Usage:
- This class can be used separately, which gives a logger instance when instantiated, default as 
log into ./Log.log, refresh at 00:00 daily, without email contact and will open a new terminal for `ERROR`
level messages.
- By default, a logger instance is created in `main.py` and is used to monitor every event within the task.
- The `_CONTACT_PARAM` can be configured with username and APP password provided by 
IMAP service, this user will be incharge of all task related emails, which will be send if any `CRITICAL`(by default)
situation is found.

### Connection.py
- Defines the `_DriverCore` class and the `DriverInit` class, 
- `_DriverCore`: The class in which the main configurations of the driver and the JavaScript code used for 
fingerprint elemination are stored, please do not modify this class.
- `DriverInit`: The class used to generate the driver instance and execute the JS code.

- ### Usage:
- Instantiate the `DriverInit`, which will return an available driver, default as Chrome driver with 
options in `_STANDARD_DRIVER_OPTIONS` and `_EXPERIMENTAL_OPTIONS`.
- Normal options can be passed by `driver_option_param`, the `headless` parameter exists individually
because of high frequency of usage.
- `insert_undefined_js` is a static method for non-chrome drivers to be in the state of undefined, which 
needes to be executed right before the core task(maybe repeatedly) to cover the driver traces.
- Notice that `_EXPERIMENTAL_OPTIONS` can only be manually added to the dict and are only available
for Chrome(Edge) core drivers.

### DriverAction.py
- Defines the `DriverAction` class, where the most commmonly used selenium driver actions are wrapped in 
functions for convient use.
- ### Usage:
- Instantiate the `DriverAction` class, give it your intened driver and By, then you can complete your 
task using whatever function in it.
- Every function which uses `self._by` by default can be redesignited with a desired one.
- `driver_signiture_validate` is a static method which test the signiture situation by vist <https://bot.sannysoft.com/>,
the default chrome driver can pass all tests, please do not modify this function.
- Notice that `window_switch` and `frame_switch` are created as function wrappers basing on the concept of
functional programming, detailed instructions are on the documentation.

### SaveToolKit.py
- Define the `SaveToolKit` class, in which you can perform save operations, supports csv and 
common database insertion for Json-like objects.
- ### Usage:
- All the methods within it are static.
- `csv_save` is async and implemented with a thread lock, be cautious when 
modifying it.
- Supported databases include `MySQL`, `MongoDB` and `Redis`, `mysql_insert` is equipped with
error rollback functionality.

### ParseToolKit.py
- Define the `ParseToolKit` class, in which you can perform parse operations for dicts and Json-like
objects.
- ### Usage:
- All the methods within it are static.
- Feel free to alter the terminal table color with `_TABLE_COLORPLAN`.
- Notice that all functions within it are not logged by default.

### Workflow.py
- This is an experimental web crawling framework, feel free to ignore it.
- Defines `Workflow` class, consists of main driver flow, parse flow and save flow.
- ### Usage
- Inherit the `Workflow` class, the default setting is using XPATH, no email contact and
default driver.
- Override the abstract method `main_driver_flow`, in which you will do most of your selenium work,
usage of `DriverAction` is  recommended.
- `parse_flow` and `save_flow` can be overrided depending on the specific task, usage of `ParseToolKit` and `SaveToolKit`
are recommended.
- `run` is a simple runner API, feel free to override and change it to whatever you like.

### For more information, please refer to the docstring within the code.