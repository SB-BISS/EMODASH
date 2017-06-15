package nl.biss.emodash;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.sql.ResultSet;
import java.sql.SQLException;

import org.json.JSONObject;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
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
		
		
	   //singleton
	   EmodashQueries qr= 	EmodashQueries.getEmodashQueryDb();
		
		//json return
		
		// select the last call id
	   
		ResultSet set = qr.emodashQuery("Select phonecall.CallId, max(phonecall.timestamp_beginning) from phonecall "
				+ "where phonecall.AgentId = '" + agent_id + "' , phonecall.CustomerId = '"+customer_id+"'" 
				+ "Group by phonecall.Callid;"); //it should only give me a result
		
		
		String callid=null;
		try {
			callid = set.getString(0);
			set.close();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
		return callid;
		
		//register here
		
	}
	
	

	@GetMapping("/get_session_id_no_customer")
	public String get_session_id_no_customer(@RequestParam("agent_id") String agent_id){
		
		//json return
		
		
		   //singleton
		   EmodashQueries qr= 	EmodashQueries.getEmodashQueryDb();
			
			//json return
			
			// select the last call id
		   
		   /*
		    * 
		    * 
		    * 
		    */
		   
			ResultSet set = qr.emodashQuery("Select phonecall.CallId, max(phonecall.timestamp_beginning) from phonecall "
					+ "where phonecall.AgentId = '" + agent_id + "'" 
					+ "Group by phonecall.Callid;"); //it should only give me a result
			
			
			String callid=null;
			try {
				callid = set.getString(0);
				set.close();
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
			
			return callid;
			
			//register here
		
	}
	
	
	
	
	
	
	@PostMapping("/get_anagraphic_data")
	public String get_anagraphic_data(@RequestBody String customer_id){
		
		//json return
		//SQL query here
		System.out.println(customer_id);
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
		
		EmodashQueries qr= 	EmodashQueries.getEmodashQueryDb();

		ResultSet set = qr.emodashQuery("Select * from customer where customer.customerId='"+ customer_id +"';");
		
		try {
			set.first();
		} catch (SQLException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}	
				
		
		try {
			
			
		 int Age=set.getInt("Age");
		 String Name=set.getString("Name");
	     String Sex=	set.getString("Sex");
		 String Surname=	set.getString("Surname");
		 String Adress=	set.getString("Adress");
		 AnagraphicData datapojo= new AnagraphicData();
			
			datapojo.setAge(Age);
			datapojo.setName(Name);
			datapojo.setGender(Sex);
			datapojo.setAdress(Adress);
			datapojo.setSurname(Surname);
			
			set.close();
			
			return datapojo;
			
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return null;
	}



	@GetMapping("/customer_emotions")
	public String customer_emotions(@RequestParam("customer_id") String customer_id, @RequestParam("call_id") String session_id){
		
		EmodashQueries qr= 	EmodashQueries.getEmodashQueryDb();

		ResultSet set = qr.emodashQuery("Select * from Emotions where Emotions.customerId='"+ customer_id +"', Emotions.callId = '" +session_id+ "';");
		
		
		//Again json list of emotions
		//query to db here.
		
		//The list should have: session id
		//Current Emotions ordered in time,
		//Just the last one !
		
		return "Cutomer_Emotions";
		
		//register here
		
	}
	
	
	@GetMapping("/agent_emotions")
	public String agent_emotions(@RequestParam("agent_id") String agent_id, @RequestParam("call_id") String session_id){
		
		EmodashQueries qr= 	EmodashQueries.getEmodashQueryDb();
		ResultSet set = qr.emodashQuery("Select * from Emotions where Emotions.customerId='"+ agent_id +"', Emotions.callId = '" +session_id+ "';");

		//The list should have: session id
		//Current Emotions ordered in time,
		//Just the last one !
		
		
		
		
		
		return "Agent_emotions";
	}
	
	

}
