## File Contents

### This is introduction of the java version selenium-up.
### Since this is not the major version, the introduction will be brief, for more information, please refer to the docstring in code.

### Logger package
- `CustomLog`: This class is made to customize the `logback.xml` setting file.
- `EmailConfig`: public class for email configuration storage, separated from `CustomLog` class for readability.
- ### Usage:
- This class can be used separately, gives a `CustomLog` instance, pass a `HashMap` of parameters which you prefer for file and terminal logger.
- `setEmail`: API built for email configuration settings, pass a `HashMap` of parameters and you intended email warning level.
- Default parameters are available inside the class, don't include them in HashMap to enable the default settings.



### For more information, please refer to the docstring within the code.