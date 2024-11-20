package logger;


public class EmailConfig {
	private String username;
    private String password;
    private String from;
    private String to;
    private String smtpHost;
    private String smtpPort;
    
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
        		if(host != null) {}
    		}
    	}catch (ArrayIndexOutOfBoundsException e) {
    		throw new WrongEmailFormatException("Please check and make sure that you input the correct email address");
		}
    }
    public EmailConfig(
    		String username, 
    		String password, 
    		String from,
    		String to, 
    		String smtpHost, 
    		String smtpPort) 
    {		
    	String [] emailStrings = {from, to};
        this.username = username;
        this.password = password;
        this.from = from;
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
    public String getFrom() {return this.from;}
    public String getTo() { return to; }
    public String getSmtpHost() { return smtpHost; }
    public String getSmtpPort() { return smtpPort; }
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

