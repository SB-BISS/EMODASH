package nl.biss.emodash;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import nl.biss.emodash.pojo.WaveWrapper;

public class ManualDebug2 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		 RestTemplate template = new RestTemplate();
         
       
         HttpHeaders headers = new HttpHeaders();
         headers.setContentType(MediaType.TEXT_PLAIN);
         
         HttpEntity<String> entity = new HttpEntity<String>("c0", headers);
         
        
         
         ResponseEntity<String> getres = template.exchange("http://localhost:8080/get_anagraphic_data",HttpMethod.POST, entity, String.class);
        
        System.out.println(getres);
      

	}

}
