package selenium;


import org.openqa.selenium.*;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Duration;
import java.util.List;
import java.util.Map;

public class DriverAction {
    private WebDriver driver;
    private static final Logger logger = LoggerFactory.getLogger(DriverAction.class);

    public DriverAction(WebDriver driver, By by, Map<String, Object> contact, String emailLevel) {
        this.driver = driver;
    }

    /**
     * Waits for a web element to be present.
     *
     * @param locator       The By locator of the element.
     * @param waitTime      Maximum time to wait in seconds.
     * @param decoratorLog  Whether to log the waiting action.
     * @return The found WebElement.
     */
    private WebElement wait(By locator, int waitTime, boolean decoratorLog) {
        try {
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(waitTime));
            WebElement element = wait.until(ExpectedConditions.presenceOfElementLocated(locator));
            if (decoratorLog) {
                logger.debug("Waited for element {}", locator);
            }
            return element;
        } catch (Exception e) {
            logger.error("Error waiting for element {}: {}", locator, e.getMessage());
            throw e;
        }
    }

    /**
     * Clicks on a web element.
     *
     * @param locator      The By locator of the element.
     * @param elementName  The name of the element for logging.
     * @param log          Whether to log the action.
     * @return A list of window handles.
     */
    public List<String> clickElement(By locator, String elementName, boolean log) {
        try {
            WebElement element = wait(locator, 20, true);
            element.click();
            if (log) {
                logger.debug("Clicked on element {}", elementName);
            }
            return List.copyOf(driver.getWindowHandles());
        } catch (Exception e) {
            logger.error("Failed to click element {}: {}", elementName, e.getMessage());
            throw e;
        }
    }

    /**
     * Double-clicks on a web element.
     *
     * @param locator      The By locator of the element.
     * @param elementName  The name of the element for logging.
     * @param log          Whether to log the action.
     * @return A list of window handles.
     */
    public List<String> doubleClick(By locator, String elementName, boolean log) {
        try {
            WebElement element = wait(locator, 20, true);
            Actions actions = new Actions(driver);
            actions.doubleClick(element).perform();
            if (log) {
                logger.debug("Double clicked on element {}", elementName);
            }
            return List.copyOf(driver.getWindowHandles());
        } catch (Exception e) {
            logger.error("Failed to double click element {}: {}", elementName, e.getMessage());
            throw e;
        }
    }

    /**
     * Right-clicks on a web element.
     *
     * @param locator      The By locator of the element.
     * @param elementName  The name of the element for logging.
     * @param log          Whether to log the action.
     * @return A list of window handles.
     */
    public List<String> rightClick(By locator, String elementName, boolean log) {
        try {
            WebElement element = wait(locator, 20, true);
            Actions actions = new Actions(driver);
            actions.contextClick(element).perform();
            if (log) {
                logger.debug("Right clicked on element {}", elementName);
            }
            return List.copyOf(driver.getWindowHandles());
        } catch (Exception e) {
            logger.error("Failed to right click element {}: {}", elementName, e.getMessage());
            throw e;
        }
    }

    /**
     * Retrieves the value of a specified attribute from a web element.
     *
     * @param locator    The By locator of the element.
     * @param attribute  The attribute name.
     * @param log        Whether to log the action.
     * @return The attribute value.
     */
    public String getElementAttribute(By locator, String attribute, boolean log) {
        try {
            WebElement element = wait(locator, 20, true);
            String result = element.getAttribute(attribute).trim();
            if (log) {
                logger.debug("Get attribute " + attribute + " on element " + locator + ", result: " + result);
            }
            return result;
        } catch (Exception e) {
            logger.error("Failed to get attribute" + attribute + "from element "+locator+": " + e.getMessage());
            throw e;
        }
    }

    /**
     * Sends keys to a web element.
     *
     * @param locator  The By locator of the element.
     * @param keys     The keys to send.
     * @param log      Whether to log the action.
     */
    public void inputKeys(By locator, String keys, boolean log) {
        try {
            WebElement element = wait(locator, 20, true);
            element.sendKeys(keys);
            if (log) {
                logger.debug("Input text '{}' into element {}", keys, locator);
            }
        } catch (Exception e) {
            logger.error("Failed to input keys into element {}: {}", locator, e.getMessage());
            throw e;
        }
    }

    /**
     * Waits for a web element to be present.
     *
     * @param locator  The By locator of the element.
     * @param waitTime Maximum time to wait in seconds.
     * @param log      Whether to log the action.
     */
    public void waitElement(By locator, int waitTime, boolean log) {
        try {
            waitElement(locator, waitTime, log);
            if (log) {
                logger.debug("Waited for element {}", locator);
            }
        } catch (Exception e) {
            logger.error("Failed to wait for element {}: {}", locator, e.getMessage());
            throw e;
        }
    }

    /**
     * Slides a web element horizontally by a specified offset.
     *
     * @param locator      The By locator of the element.
     * @param offset       The horizontal offset.
     * @param log          Whether to log the action.
     * @param slowly       Whether to perform the action slowly.
     * @param slowStep     The step size for slow movement.
     * @param slowWait     The wait time between steps in seconds.
     */
    public void slideHorizontal(By locator, int offset, boolean log, boolean slowly, int slowStep, double slowWait) {
        try {
            WebElement element = wait(locator, 20, true);
            Actions actions = new Actions(driver);
            if (!slowly) {
                actions.clickAndHold(element).moveByOffset(offset, 0).release().perform();
            } else {
                actions.clickAndHold(element).perform();
                int i = 0;
                while (i < offset) {
                    try {
                        Thread.sleep((long) (slowWait * 1000));
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        logger.error("Thread interrupted: {}", e.getMessage());
                        throw new RuntimeException(e);
                    }
                    int moveStep = Math.min(slowStep, offset - i);
                    actions.moveByOffset(moveStep, 0).perform();
                    i += moveStep;
                }
                actions.release().perform();
            }
            if (log) {
                logger.debug("Slide element {} by offset {}", locator, offset);
            }
        } catch (Exception e) {
            logger.error("Failed to slide horizontally on element {}: {}", locator, e.getMessage());
            throw e;
        }
    }

    /**
     * Scrolls the web page down.
     *
     * @param locator    The By locator of the target element (optional).
     * @param pixel      The number of pixels to scroll (optional).
     * @param sleepTime  The sleep time in seconds between scrolls.
     * @param log        Whether to log the action.
     * @param slowly     Whether to perform the scroll slowly.
     * @param slowStep   The step size for slow scrolling.
     */
    public void scrollDown(By locator, Integer pixel, double sleepTime, boolean log, boolean slowly, int slowStep) {
        try {
            JavascriptExecutor js = (JavascriptExecutor) driver;
            if (pixel != null) {
                Thread.sleep((long) (sleepTime * 4000));
                if (slowly) {
                    for (int i = 0; i < pixel; i += slowStep) {
                        int scrollAmount = Math.min(slowStep, pixel - i);
                        js.executeScript("window.scrollBy(0, " + scrollAmount + ");");
                        Thread.sleep((long) (sleepTime * 1000));
                    }
                } else {
                    js.executeScript("window.scrollBy(0, " + pixel + ");");
                }
                if (log) {
                    logger.debug("Scroll down {} pixels", pixel);
                }
            } else if (locator != null) {
                WebElement element = wait(locator, 20, true);
                if (slowly) {
                    Long currentPosition = (Long) js.executeScript("return window.pageYOffset;");
                    Long targetPosition = (long) element.getLocation().getY();
                    targetPosition = targetPosition > 200 ? targetPosition - 200 : 0;
                    while (currentPosition < targetPosition) {
                        currentPosition += slowStep;
                        if (currentPosition > targetPosition) {
                            currentPosition = targetPosition;
                        }
                        js.executeScript("window.scrollTo(0, " + currentPosition + ");");
                        Thread.sleep((long) (sleepTime * 1000));
                    }
                } else {
                    js.executeScript("arguments[0].scrollIntoView();", element);
                }
                if (log) {
                    logger.debug("Scroll down to element {}", locator);
                }
            } else {
                if (slowly) {
                    Long height = (Long) js.executeScript("return document.body.scrollHeight");
                    Long newHeight = height;
                    while (height < newHeight) {
                        for (long i = height; i < newHeight; i += slowStep) {
                            js.executeScript("window.scrollTo(0, " + i + ");");
                            Thread.sleep((long) (sleepTime * 1000));
                        }
                        height = newHeight;
                        newHeight = (Long) js.executeScript("return document.body.scrollHeight");
                    }
                } else {
                    Thread.sleep((long) (sleepTime * 4000));
                    js.executeScript("window.scrollTo(0, 10000);");
                }
                if (log) {
                    logger.debug("Scroll down to the bottom");
                }
            }
        } catch (Exception e) {
            logger.error("Failed to scroll down: {}", e.getMessage());
            throw new RuntimeException(e);
        }
    }

    /**
     * Adds cookies to the browser.
     *
     * @param cookieInstance The cookie(s) to add. Can be a single Map or a List of Maps.
     * @param log            Whether to log the action.
     */
    @SuppressWarnings("unchecked")
    public void addCookies(Object cookieInstance, boolean log) {
        try {
            if (cookieInstance instanceof Map) {
                Map<String, Object> cookie = (Map<String, Object>) cookieInstance;
                addSingleCookie(cookie, log);
            } else if (cookieInstance instanceof List) {
                List<Map<String, Object>> cookies = (List<Map<String, Object>>) cookieInstance;
                for (Map<String, Object> cookie : cookies) {
                    addSingleCookie(cookie, log);
                }
            }
        } catch (Exception e) {
            logger.error("Failed to add cookies: {}", e.getMessage());
            throw e;
        }
    }

    /**
     * Helper method to add a single cookie.
     *
     * @param cookie The cookie data.
     * @param log    Whether to log the action.
     */
    private void addSingleCookie(Map<String, Object> cookie, boolean log) {
        try {
            Cookie.Builder builder = new Cookie.Builder(cookie.get("name").toString(), cookie.get("value").toString());
            if (cookie.containsKey("domain")) {
                builder.domain(cookie.get("domain").toString());
            }
            if (cookie.containsKey("path")) {
                builder.path(cookie.get("path").toString());
            }
            if (cookie.containsKey("expiry")) {
                builder.expiresOn(new java.util.Date((Long) cookie.get("expiry") * 1000));
            }
            if (Boolean.TRUE.equals(cookie.get("secure"))) {
                builder.isSecure(true);
            }
            driver.manage().addCookie(builder.build());
            cookie.remove("expiry"); // Remove 'expiry' as per original Python logic
            if (log) {
                logger.debug("Added cookie: {}", cookie);
            }
        } catch (Exception e) {
            logger.error("Failed to add single cookie {}: {}", cookie, e.getMessage());
            throw e;
        }
    }

    /**
     * Switches between browser windows based on the provided action list.
     *
     * @param actionList The list of actions to perform. Each action can be an Integer (window index) or a Runnable.
     * @param log        Whether to log the actions.
     * @return The title of the current window after switching.
     */
    public String windowSwitch(List<Object> actionList, boolean log) {
        try {
            List<String> windowHandles = List.copyOf(driver.getWindowHandles());
            for (Object action : actionList) {
                if (action instanceof Integer) {
                    int index = (Integer) action;
                    if (index >= 0 && index < windowHandles.size()) {
                        driver.switchTo().window(windowHandles.get(index));
                        if (log) {
                            logger.debug("Switched to window {}", driver.getTitle());
                        }
                    } else {
                        throw new IndexOutOfBoundsException("Window index out of range: " + index);
                    }
                } else if (action instanceof Runnable) {
                    Runnable func = (Runnable) action;
                    func.run();
                } else {
                    throw new IllegalArgumentException("ActionList items must be either Integer or Runnable");
                }
            }
            if (log) {
                logger.debug("Window switch completed");
            }
            return driver.getTitle();
        } catch (Exception e) {
            logger.error("Failed to switch windows: {}", e.getMessage());
            throw e;
        }
    }

    /**
     * Switches between frames based on the provided action list.
     *
     * @param actionList The list of actions to perform. Each action can be a String (frame locator) or a Runnable.
     * @param log        Whether to log the actions.
     * @param customBy   The By locator to use for frame elements.
     */
    public void frameSwitch(List<Object> actionList, boolean log, By customBy) {
        try {
            for (Object action : actionList) {
                if (action instanceof String) {
                    By locator = ByLocator(customBy, (String) action);
                    WebElement frameElement = wait(locator, 20, true);
                    driver.switchTo().frame(frameElement);
                    if (log) {
                        logger.debug("Switched to frame {}", action);
                    }
                } else if (action instanceof Runnable) {
                    Runnable func = (Runnable) action;
                    func.run();
                } else {
                    throw new IllegalArgumentException("ActionList items must be either String or Runnable");
                }
            }
            if (log) {
                logger.debug("Frame switch completed");
            }
        } catch (Exception e) {
            logger.error("Failed to switch frames: {}", e.getMessage());
            throw e;
        }
    }

    /**
     * Helper method to reconstruct a By locator from a base locator and a value.
     *
     * @param baseBy The base By locator (e.g., By.id, By.name).
     * @param value  The value to locate the element.
     * @return A new By locator with the updated value.
     */
    private By ByLocator(By baseBy, String value) {
        String byType = baseBy.toString().split(":")[0].trim();
        switch (byType) {
            case "By.id":
                return By.id(value);
            case "By.name":
                return By.name(value);
            case "By.xpath":
                return By.xpath(value);
            case "By.cssSelector":
                return By.cssSelector(value);
            case "By.className":
                return By.className(value);
            case "By.linkText":
                return By.linkText(value);
            case "By.partialLinkText":
                return By.partialLinkText(value);
            case "By.tagName":
                return By.tagName(value);
            default:
                throw new IllegalArgumentException("Unsupported By type: " + byType);
        }
    }

    /**
     * Validates the Selenium WebDriver's signature by navigating to bot.sannysoft.com.
     *
     * @param driver The Selenium WebDriver instance.
     */
    public static void driverSignatureValidate(WebDriver driver) {
        Logger logger = LoggerFactory.getLogger(DriverAction.class);
        try {
            String baseUrl = "https://bot.sannysoft.com/";
            driver.get(baseUrl);
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
            wait.until(ExpectedConditions.presenceOfElementLocated(By.xpath("//*[@id=\"fp2\"]/tr[20]/td[2]")));
            List<WebElement> tds = driver.findElements(By.xpath("//*[@id=\"fp2\"]/tr/td[2]"));
            boolean allPass = true;
            for (int i = 0; i < tds.size(); i++) {
                WebElement td = tds.get(i);
                if (!"ok".equalsIgnoreCase(td.getText())) {
                    allPass = false;
                    WebElement tr = driver.findElement(By.xpath("//*[@id=\"fp2\"]/tr[" + (i + 1) + "]/td[1]"));
                    logger.warn("Selenium driver signature test failed in: {}, type: {}", tr.getText(), td.getText());
                }
            }
            if (allPass) {
                logger.info("Selenium driver signature passed");
            }
        } catch (Exception e) {
            logger.error("Driver signature validation failed: {}", e.getMessage());
            throw e;
        }
    }
}