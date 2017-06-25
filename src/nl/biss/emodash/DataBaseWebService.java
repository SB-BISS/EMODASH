package nl.biss.emodash;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.LinkedList;

import org.json.JSONObject;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.google.gson.Gson;

import nl.biss.emodash.pojo.AnagraphicData;
import nl.biss.emodash.pojo.EmotionClass;
import nl.biss.emodash.pojo.SingleEmotion;

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
	 * Get Customer Ids
	 * 
	 * @param agent_id
	 * @param customer_id
	 * @return
	 */
	
	
	@GetMapping("/get_customer_ids")
	public String get_customer_ids(){
		
	
		LinkedList<String> customerids = new LinkedList<String>();
		
	   //singleton
	   EmodashQueries qr= 	EmodashQueries.getEmodashQueryDb();
		
		//json return
		
		// select the last call id
	   
		ResultSet set = qr.emodashQuery("Select CustomerID from Customer; ");
				
		try {
			while(set.next()){
				customerids.add(set.getString("CustomerID"));	
			}
		} catch (SQLException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
		Gson gson = new Gson();
		
		String sendids = gson.toJson(customerids);
		System.out.println("IDS" + sendids);
		
		return sendids;
		
		//register here
		
	}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
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
	
	
	
	
	
	
	@GetMapping("/get_anagraphic_data")
	public String get_anagraphic_data(@RequestParam("customer_id") String customer_id){
		
		//json return
		//SQL query here
		System.out.println(customer_id);
		AnagraphicData datapojo = sql_query(customer_id);
		
		JSONObject jsonObj = new JSONObject( datapojo );
		
		return jsonObj.toString(); //will this work ok? yes it does, wit JS.
		
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
		 String Address=	set.getString("Address");
		 String Region = set.getString("Region");
		 String Postal_code = set.getString("postal_code");
		 
		 AnagraphicData datapojo= new AnagraphicData();
			
			datapojo.setAge(Age);
			datapojo.setPostalCode(Postal_code);
			datapojo.setName(Name);
			datapojo.setGender(Sex);
			datapojo.setAddress(Address);
			datapojo.setSurname(Surname);
			datapojo.setRegion(Region);
			set.close();
			
			return datapojo;
			
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return null;
	}



	@GetMapping("/customer_emotions_live")
	public String customer_emotions(@RequestParam("customer_id") String customer_id, @RequestParam("call_id") String session_id){
		
		EmodashQueries qr= 	EmodashQueries.getEmodashQueryDb();

		ResultSet set = qr.emodashQuery("Select * from Emotions where Emotions.customerId='"+ customer_id +"', Emotions.callId = '" +session_id+ "' order by Timestamp desc limit 60;");
		
		LinkedList<SingleEmotion> emotionList = new LinkedList<SingleEmotion>();
		
		try {
			if(set.getFetchSize()==0){
				
				
				return "[]";
				
			}else{
				
				
				while(set.next()){
					
					
				   String type= set.getString("EmotionType");
				   float value = set.getFloat("Value");
					
				   SingleEmotion emo= new SingleEmotion(type,value);
				   //
				   emotionList.addFirst(emo);
				   
				   
				}
				
				
				Gson gs = new Gson();
				gs.toJson(emotionList);
				
				return emotionList.toString();
				
			}
			
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		//Again json list of emotions
		//query to db here.
		
		//The list should have: session id
		//Current Emotions ordered in time,
		//Just the last one !
		
		return "[]";
		
		//register here
		
	}
	
	
	@GetMapping("/agent_emotions_live")
	public String agent_emotions(@RequestParam("agent_id") String agent_id, @RequestParam("call_id") String session_id){
		
		EmodashQueries qr= 	EmodashQueries.getEmodashQueryDb();

		ResultSet set = qr.emodashQuery("Select * from Emotions where Emotions.customerId='"+ agent_id +"', Emotions.callId = '" +session_id+ "' order by Timestamp desc limit 60;");
		
		LinkedList<SingleEmotion> emotionList = new LinkedList<SingleEmotion>();
		
		try {
			if(set.getFetchSize()==0){
				
				
				return "[]";
				
			}else{
				
				
				while(set.next()){
					
					
				   String type= set.getString("EmotionType");
				   float value = set.getFloat("Value");
					
				   SingleEmotion emo= new SingleEmotion(type,value);
				   //
				   emotionList.addFirst(emo);
				   
				   
				}
				
				
				Gson gs = new Gson();
				gs.toJson(emotionList);
				
				return emotionList.toString();
				
			}
			
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		//Again json list of emotions
		//query to db here.
		
		//The list should have: session id
		//Current Emotions ordered in time,
		//Just the last one !
		
		return "[]";
		
		//register here
		
	}
	
	

}
