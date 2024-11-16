# Selenium_up

Commonly used web crawling toolkit and Selenium API framework.

## Setup

### Install the required packages

```shell
pip install -r requirements.txt
```

### Install the Browser Drivers

```shell
python DownloadDrivers.py
```

## Contents
### Log.py
- Defines `CustomLog`, which wraps the library `loguru` and `yagmail`.
- ### Usage:
- This class can be used separately, which gives a logger instance when instantiated, default as 
log into ./Log.log, refresh at 00:00 daily, without email contact and will open a new terminal for `ERROR`
level messages
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


### SaveToolKit.py


### ParseToolKit.py



### Workflow.py
- This is an experimental web crawling framework, feel free to ignore it.
- Defines `Workflow` class, consists of main driver flow, parse flow and save flow.
- ### Usage
- Inherit the `Workflow` class, the default setting is using XPATH, no email contact and
default driver.
- Override the abstract method `main_driver_flow`, in which you will do most of your selenium work.
- `parse_flow` and `save_flow` can be overrided depending on the specific task, usage of `ParseToolKit` and `SaveToolKit`
are recommended.
- `run` is a simple runner API, feel free to override and change it to whatever you like.



## Contributing

Feel free to contribute to this project by submitting issues or pull requests. 
Your feedback and contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
