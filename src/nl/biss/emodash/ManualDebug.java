package nl.biss.emodash;

import java.io.*;

import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.UnsupportedAudioFileException;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import nl.biss.emodash.pojo.WaveWrapper;

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
	    try {
	    	

	    	File file = new File("./resources/duck.wav");
            FileInputStream fis = new FileInputStream(file);
            BufferedInputStream inputStream = new BufferedInputStream(fis);
            byte[] fileBytes = new byte[(int) file.length()];
            inputStream.read(fileBytes);
            inputStream.close();
             
            
            RestTemplate template = new RestTemplate();
            
            WaveWrapper wav = new WaveWrapper();
            
            wav.setWav_stream(fileBytes);
            
            System.err.println(fileBytes[0]);
            
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            
           String getres = template.getForObject("http://localhost:8080/init", String.class);
           
           System.out.println(getres);
           
           wav.setId("ag");
           ResponseEntity<String> response =  template.postForEntity(uri,  wav, String.class);
           

           System.out.println(response); 		
           
		    
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	    
	    
	    
	   
	    //System.out.println(result);
	}
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
			sendWav();
	}

}
