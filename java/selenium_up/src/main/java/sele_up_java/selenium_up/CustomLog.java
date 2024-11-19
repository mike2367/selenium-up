package sele_up_java.selenium_up;

import java.io.File;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.Map;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathFactory;

import org.w3c.dom.Document;
import org.w3c.dom.Node;

class CustomLog {
    
    // Custom Exception for Invalid Log Levels
    private static class LogLevelNotFoundException extends Exception {
        private static final long serialVersionUID = 1L;

        public LogLevelNotFoundException(String message) {
            super(message);
        }
    }

    // Default Logging Parameters
    private static class LogDefaultParam {
        String LOG_FILE_LOCATION = "./log-file";
        String LOG_NAME = "Log %d{yyyy-MM-dd}.log";
        String FILE_ROLLING_POLICY = "TimeBasedRollingPolicy";
        String FILE_TRIGGERING_POLICY = "SizeBasedTriggeringPolicy";
        String MAX_KEEP_DAYS = "30";
        String MAX_KEEP_SIZE = "20MB";
        String LOG_FORMAT = "%d{yyyy-MM-dd} %d{HH:mm:ss.SSS}[%-5level][%thread]%logger{36} - %msg%n";
        String ROOT_LEVEL = "debug";
        
        private static final Set<String> ALLOWED_LEVELS = new HashSet<>(
                Arrays.asList("trace", "debug", "info", "warn", "error"));

        /**
         * Default constructor initializing default parameters.
         */
        LogDefaultParam() {
        }

        /**
         * Constructor that initializes parameters based on the provided map.
         *
         * <p>The map can contain the following keys to customize the logging configuration:
         * <ul>
         *   <li><strong>logFileLocation</strong>: {@code String} - The directory path where log files will be stored. 
         *       Example: {@code "logs/custom_application.log"}</li>
         *   <li><strong>logName</strong>: {@code String} - The naming pattern for log files, supporting date placeholders. 
         *       Example: {@code "custom_Log_%d{yyyy-MM-dd}.log"}</li>
         *   <li><strong>fileRollingPolicy</strong>: {@code String} - The rolling policy for log files. 
         *       Allowed values: {@code "TimeBasedRollingPolicy"}, {@code "SizeBasedTriggeringPolicy"}.</li>
         *   <li><strong>fileTriggeringPolicy</strong>: {@code String} - The triggering policy for log file rollover. 
         *       Allowed values: {@code "TimeBasedRollingPolicy"}, {@code "SizeBasedTriggeringPolicy"}.</li>
         *   <li><strong>maxKeepDays</strong>: {@code String} - The maximum number of days to retain log files. 
         *       Example: {@code "60"}</li>
         *   <li><strong>maxKeepSize</strong>: {@code String} - The maximum size of log files before rollover occurs. 
         *       Example: {@code "50MB"}</li>
         *   <li><strong>logFormat</strong>: {@code String} - The pattern defining the format of log messages. 
         *       Example: {@code "%d{yyyy-MM-dd HH:mm:ss} [%level] [%thread] %logger{36} - %msg%n"}</li>
         *   <li><strong>rootLevel</strong>: {@code String} - The root logging level. 
         *       Allowed values: {@code "trace"}, {@code "debug"}, {@code "info"}, {@code "warn"}, {@code "error"}.</li>
         * </ul>
         *
         * @param params Map containing logging parameters.
         * @throws LogLevelNotFoundException if the provided root level is invalid.
         */
        LogDefaultParam(Map<String, String> params) throws LogLevelNotFoundException {
            if (params.containsKey("logFileLocation"))
                this.LOG_FILE_LOCATION = params.get("logFileLocation");
            if (params.containsKey("logName"))
                this.LOG_NAME = params.get("logName");
            if (params.containsKey("fileRollingPolicy"))
                this.FILE_ROLLING_POLICY = params.get("fileRollingPolicy");
            if (params.containsKey("fileTriggeringPolicy"))
                this.FILE_TRIGGERING_POLICY = params.get("fileTriggeringPolicy");
            if (params.containsKey("maxKeepDays"))
                this.MAX_KEEP_DAYS = params.get("maxKeepDays");
            if (params.containsKey("maxKeepSize"))
                this.MAX_KEEP_SIZE = params.get("maxKeepSize");
            if (params.containsKey("logFormat"))
                this.LOG_FORMAT = params.get("logFormat");
            if (params.containsKey("rootLevel")) {
                String level = params.get("rootLevel");
                if (ALLOWED_LEVELS.contains(level.toLowerCase())) {
                    this.ROOT_LEVEL = level.toLowerCase();
                } else {
                    throw new LogLevelNotFoundException(
                        "The available log levels are [\"trace\", \"debug\", \"info\", \"warn\", \"error\"], "
                        + "please check your spelling and ensure it's in lowercase.");
                }
            }
        }
    }

    private LogDefaultParam params;

    /**
     * Default constructor initializing with default parameters.
     */
    public CustomLog() {
        this.params = new LogDefaultParam();
        initializeLogger();
    }

    /**
     * Constructor that allows customization of logging parameters using a Map.
     * Pass an empty map or omit keys to keep default values.
     *
     * @param parameters Map containing logging parameters.
     * @throws LogLevelNotFoundException if the provided root level is invalid.
     */
    public CustomLog(Map<String, String> parameters) throws LogLevelNotFoundException {
        this.params = new LogDefaultParam(parameters);
        initializeLogger();
    }

    /**
     * Initializes the logger by updating the logback.xml configuration file
     * based on the current parameters.
     */
    private void initializeLogger() {
        try {
            String logbackConfigPath = "src/main/resources/logback.xml";
            File xmlFile = new File(logbackConfigPath);

            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            factory.setNamespaceAware(true);
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse(xmlFile);

            String logFileLocationExpr = "/configuration/property[@name='LOG_FILE_LOCATION']/@value";
            String logNameExpr = "/configuration/appender[@name='FILE']/fileNamePattern";
            String fileRollingPolicyExpr = "/configuration/appender[@name='FILE']/rollingPolicy/@class";
            String fileTriggeringPolicyExpr = "/configuration/appender[@name='FILE']/triggeringPolicy/@class";
            String maxKeepDaysExpr = "/configuration/appender[@name='FILE']/rollingPolicy/maxHistory";
            String maxKeepSizeExpr = "/configuration/appender[@name='FILE']/triggeringPolicy/maxFileSize";
            String logFormatExpr = "/configuration/appender[@name='FILE']/encoder/pattern";
            String rootLevelExpr = "/configuration/root/@level";


            updateNodeValue(doc,logFileLocationExpr, this.params.LOG_FILE_LOCATION);
            updateNodeValue(doc, logNameExpr, this.params.LOG_NAME);
            updateNodeValue(doc,fileRollingPolicyExpr, "ch.qos.logback.core.rolling." + this.params.FILE_ROLLING_POLICY);
            updateNodeValue(doc,fileTriggeringPolicyExpr, "ch.qos.logback.core.rolling." + this.params.FILE_TRIGGERING_POLICY);
            updateNodeValue(doc,maxKeepDaysExpr, this.params.MAX_KEEP_DAYS);
            updateNodeValue(doc,maxKeepSizeExpr, this.params.MAX_KEEP_SIZE);
            updateNodeValue(doc,logFormatExpr, this.params.LOG_FORMAT);
            updateNodeValue(doc,rootLevelExpr, this.params.ROOT_LEVEL);

            // Persist changes to logback.xml
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();

            transformer.setOutputProperty(OutputKeys.INDENT, "no");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
            DOMSource source = new DOMSource(doc);
            StreamResult result = new StreamResult(xmlFile);
            transformer.transform(source, result);

            System.out.println("logback.xml has been successfully updated with logger settings.");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Helper method to update the value of an XML node identified by an XPath expression.
     *
     * @param doc        The XML Document.
     * @param xpath      XPath instance.
     * @param expression XPath expression to locate the node.
     * @param newValue   New value to set.
     * @throws Exception if an error occurs during XPath evaluation.
     */
    private void updateNodeValue(Document doc, String expression, String newValue) throws Exception {
        
        XPathFactory xpathFactory = XPathFactory.newInstance();
        XPath xpath = xpathFactory.newXPath();
        XPathExpression expr = xpath.compile(expression);
        Node node = (Node) expr.evaluate(doc, XPathConstants.NODE);
        if (node != null) {
            node.setNodeValue(newValue);
        }
    }
    
    
    public void SetEmail(Map<String, String> emailContact, String emailLevel) 
    		throws LogLevelNotFoundException{
    	String hostString;
    	String hostPort;
    	if(emailContact.get("smtpHost") != null && emailContact.get("smtpPort") != null) {
    		hostString = emailContact.get("smtpHost");
    		hostPort = emailContact.get("smtpPort");
    	}else {
    		/** default email port setting*/
    		hostString = "smtp.gmail.com";
    		hostPort = "587";
		}
    	
    	EmailConfig config = new EmailConfig(
    			emailContact.get("username"), 
    			emailContact.get("password"), 
    			emailContact.get("from"),
    			emailContact.get("to"), 
    			hostString,
    			hostPort);
    	String logbackConfigPath = "src/main/resources/logback.xml";
        File xmlFile = new File(logbackConfigPath);
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            factory.setNamespaceAware(true);
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse(xmlFile);
            
            String base_xpathString = "/configuration/appender[@name='EMAIL']";
            String host_xpathString = base_xpathString + "/smtpHost";
            String Port_xpathString = base_xpathString + "/smtpPort";
            String user_xpathString = base_xpathString + "/username";
            String password_xpathString = base_xpathString + "/password";
            String from_xpathString = base_xpathString + "/from";
            String to_xpathString = base_xpathString + "/to";
            
            this.updateNodeValue(doc, host_xpathString, config.getHostName());
            this.updateNodeValue(doc, Port_xpathString, config.getSmtpPort());
            this.updateNodeValue(doc, user_xpathString, config.getUsername());
            this.updateNodeValue(doc, password_xpathString, config.getPassword());
            this.updateNodeValue(doc, from_xpathString, config.getFrom());
            this.updateNodeValue(doc, to_xpathString, config.getTo());
            
            // Persist changes to logback.xml
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();

            transformer.setOutputProperty(OutputKeys.INDENT, "no");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
            DOMSource source = new DOMSource(doc);
            StreamResult result = new StreamResult(xmlFile);
            transformer.transform(source, result);

            System.out.println("logback.xml has been successfully updated with email settings.");
            
            
        }catch (Exception e) {
			// TODO: handle exception
        	e.printStackTrace();
		}

    }
    
}	