package sele_up_java.selenium_up;

import java.io.File;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

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
	private static class LogLevelNotFoundException extends Exception {
		private static final long serialVersionUID = 1L;

		public LogLevelNotFoundException(String message) {
			super(message);
		}
	}

	private static class LogDefaultParam {
		String LOG_FILE_LOCATION = "./log-file";
		String LOG_NAME = "Log %d{yyyy-MM-dd}.log";
		String FILE_ROLLING_POLICY = "TimeBasedRollingPolicy";
		String FILE_TRIGGERING_POLICY = "SizeBasedTriggeringPolicy";
		String MAX_KEEP_DAYS = "30";
		String MAX_KEEP_SIZE = "20MB";
		String LOG_FORMAT = "%d{yyyy-MM-dd} %d{HH:mm:ss.SSS}" + "[%-5level][%thread]%logger{36} - %msg%n";

		String ROOT_LEVEL = "debug";
		private static final Set<String> ALLOWED_LEVELS = new HashSet<>(
				Arrays.asList("trace", "debug", "info", "warn", "error"));

		/*
		 * Default constructor
		 */
		LogDefaultParam() {
		}

		LogDefaultParam(String logFileLocation, String logName, String fileRollingPolicy, String fileTriggeringPolicy,
				String maxKeepDays, String maxKeepSize, String logFormat, String rootLevel) {

			if (logFileLocation != null)
				this.LOG_FILE_LOCATION = logFileLocation;
			if (logName != null)
				this.LOG_NAME = logName;
			if (fileRollingPolicy != null)
				this.FILE_ROLLING_POLICY = fileRollingPolicy;
			if (fileTriggeringPolicy != null)
				this.FILE_TRIGGERING_POLICY = fileTriggeringPolicy;
			if (maxKeepDays != null)
				this.MAX_KEEP_DAYS = maxKeepDays;
			if (maxKeepSize != null)
				this.MAX_KEEP_SIZE = maxKeepSize;
			if (logFormat != null)
				this.LOG_FORMAT = logFormat;
			if (rootLevel != null)
				this.ROOT_LEVEL = rootLevel;
		}

	}

	private LogDefaultParam params;

	public CustomLog() {
		this.params = new LogDefaultParam();
		initializeLogger();
	}

	private Boolean validate_level(String level) {
		Boolean contains = false;
		for (String allows_level : LogDefaultParam.ALLOWED_LEVELS) {
			if (allows_level == level) {
				contains = true;
			}
		}
		return contains;
	}

	/**
	 * Constructor that allows partial customization of logging parameters. Pass
	 * `null` for parameters you want to keep as default.
	 * 
	 * @param logFileLocation      Location of the log file.
	 * @param logName              Name pattern of the log files.
	 * @param fileRollingPolicy    Policy for rolling over log files.
	 * @param fileTriggeringPolicy Policy for triggering log file rollover.
	 * @param maxKeepDays          Maximum number of days to keep log files.
	 * @param maxKeepSize          Maximum size of log files.
	 * @param logFormat            Format of the log messages.
	 * @param rootLevel            Root logging level.
	 * @param availableLevel       Array of available logging levels.
	 */
	public CustomLog(String logFileLocation, String logName, String fileRollingPolicy, String fileTriggeringPolicy,
			String maxKeepDays, String maxKeepSize, String logFormat, String rootLevel)
			throws LogLevelNotFoundException {
		if (!validate_level(rootLevel)) {
			throw new LogLevelNotFoundException(
					"The avaliable log levels are [\"trace\", \"debug\", \"info\", \"warn\", \"error\"]"
							+ ", please check your spell, make sure it's lower case.");
		}
		this.params = new LogDefaultParam(logFileLocation, logName, fileRollingPolicy, fileTriggeringPolicy,
				maxKeepDays, maxKeepSize, logFormat, rootLevel);
		initializeLogger();

	}

	/**
	 * alter logback.xml with current parameters.
	 */
    private void initializeLogger() {
        try {
            String logbackConfigPath = "src/main/resources/logback.xml";
            File xmlFile = new File(logbackConfigPath);

            // preparations
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            factory.setNamespaceAware(true);
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse(xmlFile);
            XPathFactory xpathFactory = XPathFactory.newInstance();
            XPath xpath = xpathFactory.newXPath();

            // Define XPath expressions
            String logFileLocationExpr = "/configuration/property[@name='LOG_FILE_LOCATION']/@value";
            String logNameExpr = "/configuration/appender[@name='FILE']/fileNamePattern";
            String fileRollingPolicyExpr = "/configuration/appender[@name='FILE']/rollingPolicy/@class";
            String fileTriggeringPolicyExpr = "/configuration/appender[@name='FILE']/triggeringPolicy/@class";
            String maxKeepDaysExpr = "/configuration/appender[@name='FILE']/rollingPolicy/maxHistory";
            String maxKeepSizeExpr = "/configuration/appender[@name='FILE']/triggeringPolicy/maxFileSize";
            String logFormatExpr = "/configuration/appender[@name='FILE']/encoder/pattern";
            String rootLevelExpr = "/configuration/root/@level";

            // file loc
            XPathExpression expr = xpath.compile(logFileLocationExpr);
            Node node = (Node) expr.evaluate(doc, XPathConstants.NODE);
            if (node != null) {
                node.setNodeValue(this.params.LOG_FILE_LOCATION);
            }
            // log name
            expr = xpath.compile(logNameExpr);
            node = (Node) expr.evaluate(doc, XPathConstants.NODE);
            if (node != null) {
                node.setNodeValue(this.params.LOG_NAME);
            }
            // rolling policy
            expr = xpath.compile(fileRollingPolicyExpr);
            node = (Node) expr.evaluate(doc, XPathConstants.NODE);
            if (node != null) {
                node.setNodeValue("ch.qos.logback.core.rolling." + this.params.FILE_ROLLING_POLICY);
            }
            // triggering policy
            expr = xpath.compile(fileTriggeringPolicyExpr);
            node = (Node) expr.evaluate(doc, XPathConstants.NODE);
            if (node != null) {
                node.setNodeValue("ch.qos.logback.core.rolling." + this.params.FILE_TRIGGERING_POLICY);
            }
            // max keep days
            expr = xpath.compile(maxKeepDaysExpr);
            node = (Node) expr.evaluate(doc, XPathConstants.NODE);
            if (node != null) {
                node.setNodeValue(this.params.MAX_KEEP_DAYS);
            }
            // max keep size
            expr = xpath.compile(maxKeepSizeExpr);
            node = (Node) expr.evaluate(doc, XPathConstants.NODE);
            if (node != null) {
                node.setNodeValue(this.params.MAX_KEEP_SIZE);
            }
            // log format
            expr = xpath.compile(logFormatExpr);
            node = (Node) expr.evaluate(doc, XPathConstants.NODE);
            if (node != null) {
                node.setNodeValue(this.params.LOG_FORMAT);
            }
            // root level
            expr = xpath.compile(rootLevelExpr);
            node = (Node) expr.evaluate(doc, XPathConstants.NODE);
            if (node != null) {
                node.setNodeValue(this.params.ROOT_LEVEL);
            }

            /**
            * Add this block to persist changes to the file
            */
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            // format the XML output
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
            DOMSource source = new DOMSource(doc);
            StreamResult result = new StreamResult(xmlFile);
            transformer.transform(source, result);

            System.out.println("logback.xml has been successfully updated.");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}