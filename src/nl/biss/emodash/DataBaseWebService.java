package nl.biss.emodash;

import java.io.FileNotFoundException;
import java.io.PrintWriter;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DataBaseWebService {
	
	
	@GetMapping("/get_anagraphic_data")
	public String register_annotator_address(@RequestParam("customer_id") String customer_id){
		
		//json return
		
		return "id";
		
		//register here
		
	}
	
	
	@GetMapping("/customer_emotions")
	public String customer_emotions(@RequestParam("customer_id") String customer_id, @RequestParam("session_id") String session_id){
		
		//Again json list of emotions
		//query to db here.
		
		return "Cutomer_Emotions";
		
		//register here
		
	}
	
	
	@GetMapping("/agent_emotions")
	public String agent_emotions(@RequestParam("agent_id") String customer_id, @RequestParam("session_id") String session_id){
		
		
		
		return "Agent_emotions";
	}
	
	

}
