package sele_up_java.selenium_up;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class LogTest {

	public static void main(String[] args) {
		
		try {
			CustomLog c_log = new CustomLog(null, null, null, null, null, null, null, "trace");
		}catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		}
		Logger logger = LoggerFactory.getLogger("logback");
		System.out.println("----> logback start");
		logger.trace("--> Hello trace.");
		logger.debug("--> Hello debug.");
		logger.info("--> Hello info.");
		logger.warn("--> Goodbye warn.");
		logger.error("--> Goodbye error.");
		System.out.println("----> logback end");
	}
}
