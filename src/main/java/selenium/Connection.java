package selenium;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.chrome.ChromeDriverService;
import org.openqa.selenium.firefox.GeckoDriverService;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Connection {
    private static final Logger logger = LoggerFactory.getLogger(Connection.class);
    
    private static final List<String> STANDARD_DRIVER_OPTIONS = List.of(
        "--incognito",
        "--disable-gpu",
        "--disable-blink-features=AutomationControlled"
    );
    private static final Map<String, String> DRIVER_PATHS = Map.of(
            "Chrome", "src/main/resources/chrome/chromedriver.exe",   // Update the path as per your environment
            "Firefox", "src/main/resources/firefox/geckodriver.exe" // Update the path as per your environment
       );

    /**
     * Experimental options require being manually added to the map and are only suitable for Chrome driver
     */
    private static final Map<String, Object> EXPERIMENTAL_OPTIONS = Map.of(
    	"detach", true,
    	"excludeSwitches", List.of("enable-automation", "enable-logging")
	);
    private static class DriverCore {
        private String seleniumDriverType;
        private List<String> optParams;
        private String scriptFunc = "Page.addScriptToEvaluateOnNewDocument";
        private String CHR_mem_js = 
            "Object.defineProperty(navigator, 'deviceMemory', {\n" +
            "    get: () => 8\n" +
            "});\n" +
            "Object.defineProperty(navigator, 'userAgent', {\n" +
            "    get: () => 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'\n" +
            "});\n";
        private String undefined_js = 
            "Object.defineProperty(navigator, 'webdriver', {\n" +
            "    get: () => undefined\n" +
            "});";
        private String stealth_js;

        public DriverCore(String seleniumDriverType, List<String> driverOptionParam, boolean headless) {
            this.seleniumDriverType = seleniumDriverType;
            this.optParams = new ArrayList<>(STANDARD_DRIVER_OPTIONS);
            if (driverOptionParam != null) {
                this.optParams.addAll(driverOptionParam);
            }
            if (headless) {
                this.optParams.add("--headless");
            }
            // Remove duplicates
            Set<String> uniqueOptions = new HashSet<>(this.optParams);
            this.optParams = new ArrayList<>(uniqueOptions);

            // Load stealth_js from file
            try {
                this.stealth_js = Files.readString(Paths.get("src/main/resources/stealth.min.js"));
            } catch (IOException e) {
                logger.error("Failed to read stealth.min.js", e);
                this.stealth_js = "";
            }
        }

        @Override
        public String toString() {
            String driverInfo = String.format("WebDriver: %s\nDriverOptions: %s", seleniumDriverType, optParams);
            logger.info("Driver info: {}", driverInfo);
            return "-".repeat(100);
        }

    }

    public static class DriverInit {
        private DriverCore driverCore;
        private WebDriver driver;

        public DriverInit(String seleniumDriverType, List<String> driverOptionParam, boolean headless) {
            this.driverCore = new DriverCore(seleniumDriverType, driverOptionParam, headless);
            this.driver = initializeDriver();
        }

        private WebDriver initializeDriver() {
            if ("Chrome".equalsIgnoreCase(driverCore.seleniumDriverType)) {
            	
                ChromeOptions options = new ChromeOptions();

                for (String option : driverCore.optParams) {
                    options.addArguments(option);
                }
                for (Map.Entry<String, Object> entry : EXPERIMENTAL_OPTIONS.entrySet()) {
                    options.setExperimentalOption(entry.getKey(), entry.getValue());
                }
                ChromeDriverService service = new ChromeDriverService.Builder()
                        .usingDriverExecutable(Paths.get(DRIVER_PATHS.get("Chrome")).toFile())
                        .usingAnyFreePort()
                        .build();
                WebDriver driver = new ChromeDriver(service, options);
                if (driver != null) {
                    applyStealthScripts(driver);
                    logger.info("Selenium driver successfully initialized");
                    System.out.println(driverCore);
                    return driver;
                }
            } else if ("Firefox".equalsIgnoreCase(driverCore.seleniumDriverType)) {
                FirefoxOptions options = new FirefoxOptions();
                for (String option : driverCore.optParams) {
                    options.addArguments(option);
                }
                GeckoDriverService service = new GeckoDriverService.Builder()
                        .usingDriverExecutable(Paths.get(DRIVER_PATHS.get("Firefox")).toFile())
                        .usingAnyFreePort()
                        .build();
				
                WebDriver driver = new FirefoxDriver(service, options);
                if (driver != null) {
                    applyStealthScripts(driver);
                    logger.info("Selenium driver successfully initialized");
                    System.out.println(driverCore);
                    return driver;
                }
            }
            return null;
        }

        /**
         * Applies the stealth JavaScript scripts to the WebDriver instance.
         *
         * @param driver The WebDriver instance to apply scripts to.
         */
        private void applyStealthScripts(WebDriver driver) {
            try {
                if (driver instanceof ChromeDriver) {
                    // For ChromeDriver, use executeCdpCommand
                    ChromeDriver chromeDriver = (ChromeDriver) driver;
                    chromeDriver.executeCdpCommand(driverCore.scriptFunc, Map.of("source", driverCore.stealth_js));
                    chromeDriver.executeCdpCommand(driverCore.scriptFunc, Map.of("source", driverCore.undefined_js));
                    chromeDriver.executeCdpCommand(driverCore.scriptFunc, Map.of("source", driverCore.CHR_mem_js));
                } else {
                    // For other drivers, use JavascriptExecutor
                    JavascriptExecutor jsExecutor = (JavascriptExecutor) driver;
                    jsExecutor.executeScript(driverCore.stealth_js);
                    jsExecutor.executeScript(driverCore.undefined_js);
                    jsExecutor.executeScript(driverCore.CHR_mem_js);
                }
            } catch (Exception e) {
                logger.error("Failed to apply stealth scripts", e);
            }
        }

        /**
         * This function is explicitly used for non-Chrome browsers to eliminate driver signature
         * and is required to be executed every time close to the validation
         *
         * @param driver The WebDriver instance to inject the script into.
         */
        public static void insertUndefinedJs(WebDriver driver) {
            String undefinedJs = 
                "Object.defineProperty(navigator, 'webdriver', {\n" +
                "    get: () => undefined\n" +
                "});";
            try {
                JavascriptExecutor jsExecutor = (JavascriptExecutor) driver;
                jsExecutor.executeScript(undefinedJs);
            } catch (Exception e) {
                logger.error("Failed to insert undefined_js", e);
            }
        }

        @Override
        public String toString() {
            return driverCore.toString();
        }

        public WebDriver getDriver() {
            return this.driver;
        }
    }
}