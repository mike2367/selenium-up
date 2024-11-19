package logger;



import java.util.HashMap;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class LogTest {

    static void testSetEmailWithAllParameters() throws Exception {
        Map<String, String> emailContact = new HashMap<>();
        emailContact.put("smtpHost", "smtp@test.com");
        emailContact.put("smtpPort", "465");
        emailContact.put("username", "test_user");
        emailContact.put("password", "test_pass");
        emailContact.put("from", "sender@test.com");
        emailContact.put("to", "recipient@test.com");

        String emailLevel = "error";
        
        Map<String, String> logParams = new HashMap<>();
        logParams.put("logFileLocation", "5555555555555555.log");
        logParams.put("logName", "3333333333333333.log");
        logParams.put("fileRollingPolicy", "11111111111111Policy");
        logParams.put("fileTriggeringPolicy", "22222222222Policy");
        logParams.put("maxKeepDays", "60");
        logParams.put("maxKeepSize", "50MB");
        logParams.put("logFormat", "%d{yyyy-MM-dd HH:mm:ss} [%level] [%thread] %logger{36} - %msg%n");
        logParams.put("rootLevel", "error");

        CustomLog loggerCustomLog = new CustomLog(logParams);
        loggerCustomLog.setEmail(emailContact, emailLevel);
    }


	public static void main(String[] args) throws Exception {
		
//		try {
//			CustomLog c_log = new CustomLog(null, null, null, null, null, null, null, "trace");
//		}catch (Exception e) {
//			e.printStackTrace();
//		}
//		Logger logger = LoggerFactory.getLogger("logback");
//		System.out.println("----> logback start");
//		logger.trace("--> Hello trace.");
//		logger.debug("--> Hello debug.");
//		logger.info("--> Hello info.");
//		logger.warn("--> Goodbye warn.");
//		logger.error("--> Goodbye error.");
//		System.out.println("----> logback end");
		
//		EmailConfig email = new EmailConfig(
//				"1", "2","3", "4", 587
//				);
//		email.getHostName();

		testSetEmailWithAllParameters();
	}
}

