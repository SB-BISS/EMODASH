package nl.biss.emodash;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.HashMap;
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
	   EmodashQueries qr=  new	EmodashQueries();
		
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
		
		try {
			set.close();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		qr.connectionClose();
		return sendids;
		
		//register here
		
	}
	
	/**
	 * 
	 * This has to be created before each session begins. A session represent
	 * the act of starting a call with an agent.
	 * 
	 * 
	 * 
	 * @param SessionID
	 * @param AgentID
	 * @param CustomerID
	 */

	@GetMapping("/create_call")
	public void create_call(@RequestParam("call_id") String CallID, @RequestParam("agent_id") String AgentID, @RequestParam("customer_id") String CustomerID){
		
			
		   System.err.println("CREATING CALL!");
		   EmodashQueries qr= new EmodashQueries();
		   
		   long timestamp_beginning = System.currentTimeMillis();
		   
		   qr.insertCallId(CallID, AgentID, CustomerID, timestamp_beginning);
		
		   qr.connectionClose();
		
	}
	
	/**
	 * 
	 * This has to be created before each session begins. A session represent
	 * the act of starting a call with an agent.
	 * 
	 * 
	 * 
	 * @param SessionID
	 * @param AgentID
	 * @param CustomerID
	 */

	@GetMapping("/end_call")
	public void end_call(@RequestParam("call_id") String CallID, @RequestParam("agent_id") String AgentID, @RequestParam("customer_id") String CustomerID){
		
			
		   System.err.println("Ending CALL!");
		   EmodashQueries qr= new	EmodashQueries();
		   
		   long timestamp_end = System.currentTimeMillis();
		   
		   qr.endCallId(CallID, AgentID, CustomerID, timestamp_end);
		
		   ResultSet setCustomer =qr.emodashQuery(" select emotions.emotiontype, sum(value) as totalvalue from emotions, voicesignals where emotions.streamid=voicesignals.streamid and voicesignals.personid = '"+ CustomerID+ "' group by emotiontype;");
		   ResultSet setAgent =qr.emodashQuery(" select emotions.emotiontype, sum(value) as totalvalue from emotions, voicesignals where emotions.streamid=voicesignals.streamid and voicesignals.personid = '"+ AgentID+ "' group by emotiontype;");

		   
		   
		   float total_customer = 0;
		   float total_agent = 0;
		   
		   HashMap<String,Float> map_customer = new HashMap<String,Float>();

		   HashMap<String,Float> map_agent = new HashMap<String,Float>();
		   
		   try {
			while(setCustomer.next()){
				   
				String label=  setCustomer.getString("emotiontype");
				float value = setCustomer.getFloat("totalvalue");
				
				total_customer += value;
				map_customer.put(label, value);
				   
			   }
			while(setAgent.next()){
				   
				String label=  setAgent.getString("emotiontype");
				float value = setAgent.getFloat("totalvalue");
				
				total_agent += value;
				map_agent.put(label, value);
				   
			   }
			
			
			
		   } catch (SQLException e) {
			   // TODO Auto-generated catch block
			   e.printStackTrace();
		   }
		   
		   
		   float percentage_anger_customer = map_customer.get("anger")/total_customer;
		   float percentage_disgust_customer = map_customer.get("disgust")/total_customer;
		   float percentage_fear_customer = map_customer.get("fear")/total_customer;
		   float percentage_happiness_customer = map_customer.get("happiness")/total_customer;
		   float percentage_neutral_customer = map_customer.get("neutral")/total_customer;
		   float percentage_sadness_customer = map_customer.get("sadness")/total_customer;
		   float percentage_surprise_customer = map_customer.get("surprise")/total_customer;
		   
		   float percentage_anger_agent = map_agent.get("anger")/total_agent;
		   float percentage_disgust_agent = map_agent.get("disgust")/total_agent;
		   float percentage_fear_agent = map_agent.get("fear")/total_agent;
		   float percentage_happiness_agent = map_agent.get("happiness")/total_agent;
		   float percentage_neutral_agent = map_agent.get("neutral")/total_agent;
		   float percentage_sadness_agent = map_agent.get("sadness")/total_agent;
		   float percentage_surprise_agent = map_agent.get("surprise")/total_agent;
		   
		   
		   qr.emodashUpdate("insert into emotion_history (CustomerId, CallId, anger_percentage, disgust_percentage,fear_percentage,happiness_percentage,neutral_percentage,sadness_percentage,surprise_percentage) "
		   		+ "values('"+CustomerID +"','" + CallID+"'," + percentage_anger_customer + "," + percentage_disgust_customer+ "," + percentage_fear_customer + "," +percentage_happiness_customer + ","+percentage_neutral_customer+","+percentage_sadness_customer+","+ percentage_surprise_customer+ ");");
		   qr.emodashUpdate("insert into emotion_history (CustomerId, CallId, anger_percentage, disgust_percentage,fear_percentage,happiness_percentage,neutral_percentage,sadness_percentage,surprise_percentage) "
		   		+ "values('"+AgentID +"','" + CallID+"'," + percentage_anger_agent + "," + percentage_disgust_agent+ "," + percentage_fear_agent + "," +percentage_happiness_agent + ","+percentage_neutral_agent+","+percentage_sadness_agent+","+ percentage_surprise_agent + ");");

		   qr.connectionClose();
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
	
	
	@GetMapping("/get_call_id_with_customer")
	public String get_session_id_with_customer(@RequestParam("agent_id") String agent_id, @RequestParam("customer_id") String customer_id){
		
		
	   //singleton
	   EmodashQueries qr= new 	EmodashQueries();
		
		//json return
		
		// select the last call id
	   
		ResultSet set = qr.emodashQuery("Select phonecall.CallId, phonecall.timestamp_beginning from phonecall "
				+ "where phonecall.AgentId = '" + agent_id + "' and phonecall.CustomerId = '"+customer_id+"' order by phonecall.timestamp_beginning DESC limit 1" 
				+ ";"); //it should only give me a result
		
			String callid=null;
		try {
			
			//I want the first one if it is there.
			if(set.next());
			else return null;
			
			callid = set.getString("CallId");
			set.close();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		Gson gson = new Gson();
		HashMap<String, String> map = new HashMap<String,String>();
		
		map.put("call_id", callid);
		qr.connectionClose();
		return gson.toJson(map);
		
		//register here
		
	}
	
	

	@GetMapping("/get_call_id_no_customer")
	public String get_session_id_no_customer(@RequestParam("agent_id") String agent_id){
		
		//json return
		
		
		   //singleton
		   EmodashQueries qr=  new	EmodashQueries();
			
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
			
			qr.connectionClose();
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
		
		EmodashQueries qr= new	EmodashQueries();

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
		
			set.close(); //CLOSE
			qr.connectionClose();
			return datapojo;
			
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return null;
	}

	
	
	
	@GetMapping("/customer_lastcall")
	public String customer_lastcall_emotions(@RequestParam("customer_id") String customer_id){
		
		EmodashQueries qr= 	new EmodashQueries();
		ResultSet set= qr.emodashQuery("Select "
				+ "anger_percentage ,"
				+ "disgust_percentage ,"
				+ "fear_percentage, "
				+ "happiness_percentage ,"
				+ "neutral_percentage , "
				+ "sadness_percentage , "
				+ "surprise_percentage, "
				+ "max(phonecall.timestamp_end)"  +
		" from emotion_history, phonecall "
		+ "where emotion_history.customerId='"+ customer_id +"' and "
				+ "phonecall.callid = emotion_history.callid"
				+ " group by timestamp_end;");
		
		HashMap<String,Float> fl = new HashMap<String,Float>();
		
		try {
			while(set.next()){
				
				fl.put("anger",set.getFloat("anger_percentage"));
				fl.put("disgust",set.getFloat("disgust_percentage"));
				fl.put("fear",set.getFloat("fear_percentage"));
				fl.put("happiness",set.getFloat("happiness_percentage"));
				fl.put("neutral",set.getFloat("neutral_percentage"));
				fl.put("sadness",set.getFloat("sadness_percentage"));
				fl.put("surprise",set.getFloat("surprise_percentage"));
				
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		Gson gson = new Gson();
		
		String tosubmit = gson.toJson(fl);
		qr.connectionClose();
		return tosubmit;
	}
	
	
	/**
	 * Redirection with different paramters to the method above.
	 * @param agent_id
	 * @return
	 */

	@GetMapping("/agent_lastcall")
	public String agent_lastcall_emotions(@RequestParam("agent_id") String agent_id){
		
		
		return customer_lastcall_emotions(agent_id);
	}
	
	
	
	
	


	@GetMapping("/customer_emotions_live")
	public String customer_emotions(@RequestParam("customer_id") String customer_id, @RequestParam("call_id") String call_id){
		
		EmodashQueries qr= 	new EmodashQueries();

		ResultSet set = qr.emodashQuery("Select emotiontype,value from Emotions, voicesignals where Emotions.StreamId=voicesignals.StreamId and voicesignals.PersonId='"+ customer_id +"' and Emotions.callId = '" +call_id+ "' order by Timestamp desc limit 70;");
		
		
		LinkedList<SingleEmotion> emotionList = new LinkedList<SingleEmotion>();
		
		try {
						
				while(set.next()){
					
					
				   String type= set.getString("EmotionType"); // to be shown by type
				   float value = set.getFloat("Value");
					
				   SingleEmotion emo= new SingleEmotion(type,value);
				   //
				   emotionList.addFirst(emo);
				  
				}
				
				set.close(); // CLOSE
				qr.connectionClose();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		Gson gs = new Gson();
		String emotionsJsonList= gs.toJson(emotionList);
		
		return emotionsJsonList;
		
		//register here
		
	}
	
	
	@GetMapping("/agent_emotions_live")
	public String agent_emotions(@RequestParam("agent_id") String agent_id, @RequestParam("call_id") String session_id){
		
		String agent_em = customer_emotions(agent_id,session_id);
		System.err.println(agent_em);
		return agent_em;
		
		/*EmodashQueries qr= 	EmodashQueries.getEmodashQueryDb();

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
				
				
				set.close();//CLOSE
				
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
		*/
	}
	

}
