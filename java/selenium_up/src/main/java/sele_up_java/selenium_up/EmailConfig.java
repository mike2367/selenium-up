package sele_up_java.selenium_up;

import javax.net.ssl.HostnameVerifier;
import javax.xml.crypto.dsig.dom.DOMValidateContext;

import com.google.common.net.HostAndPort;

public class EmailConfig {
	private String username;
    private String password;
    private String to;
    private String smtpHost;
    private int smtpPort;
    
    private static class WrongEmailFormatException extends Exception {
    	private static final long serialVersionUID = 1L;

    	public WrongEmailFormatException(String message) {
    		super(message);
    	}
    }
    
    private void validate(String[] address) throws WrongEmailFormatException{
    	try {
    		for(String addrString: address) {
        		String host = addrString.split("@")[1];
    		}
    	}catch (ArrayIndexOutOfBoundsException e) {
    		throw new WrongEmailFormatException("Please check and make sure that you input the correct email address");
		}
    }
    public EmailConfig(
    		String username, 
    		String password, 
    		String to, 
    		String smtpHost, 
    		int smtpPort) 
    {		
    	String [] emailStrings = {username, to, smtpHost};
        this.username = username;
        this.password = password;
        this.to = to;
        this.smtpHost = smtpHost;
        try {
            this.validate(emailStrings);
		} catch (Exception e) {
			e.printStackTrace();
		}

        this.smtpPort = smtpPort;
    }

    // Getters
    public String getUsername() { return username; }
    public String getPassword() { return password; }
    public String getTo() { return to; }
    public String getSmtpHost() { return smtpHost; }
    public int getSmtpPort() { return smtpPort; }
    public String getHostName() {
        	return this.smtpHost.split("@")[1];
    }

    @Override
    public String toString() {
        return "EmailConfig{" +
                "username='" + username + '\'' +
                ", to='" + to + '\'' +
                '}';
    }
}
