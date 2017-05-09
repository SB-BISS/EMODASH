package nl.biss.emodash;

import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

public class ManualDebug {

	/**
	 * 
	 * Manual debugging, this should 
	 * become a JUnit test as soon as possible.
	 * 
	 */
	
	private static void sendWav() {
	    final String uri = "http://localhost:8080/post_wave_agent/";
	    
	    //send the wave file
	    
	   
	    //System.out.println(result);
	}
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
