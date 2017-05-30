package nl.biss.emodash;

import java.io.FileNotFoundException;
import java.io.PrintWriter;

import org.json.JSONObject;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import nl.biss.emodash.pojo.AnagraphicData;

@RestController
public class DataBaseWebService {
	
	
	
	/**
	 * 
	 * First:
	 * session id
	 * anagraphical data
	 * Previous interaction history
	 * 
	 * 
	 * Current emotion every second (currently we get all the emotions, we should use the time stamp)
	 * 
	 * @param agent_id
	 * @param customer_id
	 * @return
	 */
	
	
	@GetMapping("/get_session_id_with_customer")
	public String get_session_id_with_customer(@RequestParam("agent_id") String agent_id, @RequestParam("customer_id") String customer_id){
		
		//json return
		
		//it is always going to return id1
		
		
		
		
		return "id1";
		
		//register here
		
	}
	
	

	@GetMapping("/get_session_id_no_customer")
	public String get_session_id_no_customer(@RequestParam("agent_id") String agent_id){
		
		//json return
		
		return "id";
		
		//register here
		
	}
	
	
	
	
	
	
	@GetMapping("/get_anagraphic_data")
	public String get_anagraphic_data(@RequestParam("customer_id") String customer_id){
		
		//json return
		//SQL query here
		AnagraphicData datapojo = sql_query(customer_id);
		
		JSONObject jsonObj = new JSONObject( datapojo );
		
		return jsonObj.toString(); //will this work ok?
		
		//register here
	}
	
	
	/**
	 * STUB for SQL query 1
	 * @param customer_id
	 * @return
	 */
	
	private AnagraphicData sql_query(String customer_id) {
		// TODO Auto-generated method stub
		
		AnagraphicData datapojo= new AnagraphicData();
		
		datapojo.setAge(35);
		datapojo.setName("Jane");
		datapojo.setGender("Female");
		
		
		return datapojo;
	}



	@GetMapping("/customer_emotions")
	public String customer_emotions(@RequestParam("customer_id") String customer_id, @RequestParam("session_id") String session_id){
		
		//Again json list of emotions
		//query to db here.
		
		//The list should have: session id
		//Current Emotions ordered in time,
		//Just the last one !
		
		return "Cutomer_Emotions";
		
		//register here
		
	}
	
	
	@GetMapping("/agent_emotions")
	public String agent_emotions(@RequestParam("agent_id") String customer_id, @RequestParam("session_id") String session_id){
		
		

		//The list should have: session id
		//Current Emotions ordered in time,
		//Just the last one !
		
		return "Agent_emotions";
	}
	
	

}
