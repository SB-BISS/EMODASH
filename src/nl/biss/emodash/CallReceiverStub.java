package nl.biss.emodash;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.LinkedList;
import java.util.UUID;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.FutureTask;

import org.json.JSONObject;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import nl.biss.emodash.pojo.EmotionClass;
import nl.biss.emodash.pojo.WaveWrapper;

import java.util.Base64;
/**
 * 
 * Assumptions: 
 * 
 * 1 Webservice to receive the things
 * 1 data base
 * No focus on Security aspects (authentication, sanitazing) 
 * 
 * @author Stefano
 *
 */



@RestController
public class CallReceiverStub {
	
	static String location_annotator = "http://localhost:50000/upload";
	
	
	
	
	@GetMapping("/init")
	public String init(){
		
		System.out.println("I EXIST");
		
		return "Ja, Zeker";
	}
	
	
	
	/**
	 * Work around string based. I have a reason to have the same code for agent and customer
	 * both, the files have to be run in parallel, EXACTLY at the same time and it really becomes difficult with one method.
	 * 
	 * 
	 * @param file
	 * @return
	 */
	
	@PostMapping(value="/post_wave_agent_string") 
	public String AgentChannelProcessingString(@RequestBody String file) {
		
	ExecutorService executor = Executors.newSingleThreadExecutor(); //to allow for a faster return to the python service
		
		//Asynchronous return
		FutureTask<String> future =  new FutureTask<String>(new Callable<String>() {
	         public String call() {
	        	 
	        	JSONObject jsonObject = new JSONObject(file);
	     		String Base64P= jsonObject.getString("wav_stream"); //base64 from Python
	     		byte[] bytes=  Base64.getDecoder().decode(Base64P);
	     		
	     		
	     		String agentid=jsonObject.getString("id");
	     		//the call id must be assigned externally
	     		String callid = jsonObject.getString("callId");;
	     		

	        	long timestamp = System.currentTimeMillis();
	     		
	     		//most important one
	     		EmotionClass emo_annotations  = get_annotations("agent",bytes); //simply apply the model.
	     		
	     		//we need to accept the situation in which the annotations may fail. Each of the annotations
	     		//should be handled asynchronously
	     		//send it to the storing services
	     		String chunkid = record_file(callid,bytes, agentid, timestamp); //chunkid must be assigned by the database.
	     		record_annotations(chunkid,agentid, emo_annotations,timestamp); //this has to be sent to the WS for storing the data
	     		// for modularity purposes we shall have it in a different WS
				return chunkid;
	     		
	         
	         }});
		executor.execute(future);
		
				
			
		
		return "ok";

	}	
	


	/**
	 * Work around string based.
	 * @param file
	 * @return
	 */
	
	@PostMapping("/post_wave_customer_string")
	public String CustomerChannelProcessing(@RequestBody String file){
		
		//System.err.print(file);

		
		
		// ->
		//  annotate(file)
		
		//it should get a time stamp too, starting from here
		//for a matter of synch problems
		
		ExecutorService executor = Executors.newSingleThreadExecutor(); //to allow for a faster return to the python service
		
		//Asynchronous return
		FutureTask<String> future =  new FutureTask<String>(new Callable<String>() {
	         public String call() {
	        	 
	        	JSONObject jsonObject = new JSONObject(file);
	     		String Base64P= jsonObject.getString("wav_stream"); //base64 from Python
	     		byte[] bytes=  Base64.getDecoder().decode(Base64P);
	     		
	     		
	     		String agentid=jsonObject.getString("id");
	     		//the call id must be assigned externally
	     		String callid = jsonObject.getString("callId");;
	     		

	        	long timestamp = System.currentTimeMillis();
	     		
	     		//most important one
	     		EmotionClass emo_annotations  = get_annotations("customer",bytes); //simply apply the model.
	     		
	     		//we need to accept the situation in which the annotations may fail. Each of the annotations
	     		//should be handled asynchronously
	     		//send it to the storing services
	     		String chunkid = record_file(callid,bytes, agentid, timestamp); //chunkid must be assigned by the database.
	     		record_annotations(chunkid,agentid, emo_annotations,timestamp); //this has to be sent to the WS for storing the data
	     		// for modularity purposes we shall have it in a different WS
				return chunkid;
	     		
	         
	         }});
		executor.execute(future);
		
				
		
		return "ok";
		
	}
	
	
	
	
	/**
	 * 
	 * Channel of the caller agent, the file posted should be a wave file
	 * the agent id should be included.
	 * 
	 */
	
	
	@RequestMapping(value="/post_wave_agent", method=RequestMethod.POST,  consumes = MediaType.APPLICATION_JSON_VALUE) 
	public String AgentChannelProcessing(@RequestBody WaveWrapper file) {

		//we shall pass through the annotation service, then store the file
		
		
		String agentid=file.getId();
		//the call id must be assigned externally
		String callid = file.getCallId();
		
		// ->
		//  annotate(file)
		
		//it should get a time stamp too, starting from here
		//for a matter of synch problems
		
		long timestamp = System.currentTimeMillis();
		
		//most important one
		EmotionClass emo_annotations  = get_annotations("agent",file.getWav_stream()); //simply apply the model.
		//we need to accept the situation in which the annotations may fail. Each of the annotations
		//should be handled asynchronously
		//send it to the storing services
		String chunkid = record_file(callid,file.getWav_stream(), agentid, timestamp); //chunkid must be assigned by the database.
		record_annotations(chunkid,agentid, emo_annotations,timestamp); //this has to be sent to the WS for storing the data
		// for modularity purposes we shall have it in a different WS
		
		
        return "Success";
    }
	
	/**
	 * Duplicated method: we want to distinguish the customer and agent channel.
	 * In the future they may need a different way to be handled.
	 * 
	 * @param file
	 * @return
	 */
	
	
	
	@PostMapping("/post_wave_customer")
	public String CustomerChannelProcessing(@RequestBody WaveWrapper file){

		//we shall have a channel for the customer too.
		//here we expect a wav file of about 4 seconds.
		//same process as for the agent, but associated to the customer
		//ASSUMPTION: we know the customer id at this point in time.
		
		String customerid=file.getId();
		String callid= file.getCallId();
		
		// ->
		//  annotate(file)
		
		//it should get a time stamp too, starting from here
		//for a matter of synch problems
		
		long timestamp = System.currentTimeMillis();
		
		//most important one
		EmotionClass emo_annotations  = get_annotations("customer",file.getWav_stream()); 
		//we need to accept the situation in which the annotations may fail. Each of the annotations
		//should be handled asynchronously
		//send it to the storing services
		String chunkid = record_file(callid,file.getWav_stream(), customerid, timestamp);
		record_annotations(chunkid,customerid, emo_annotations,timestamp); //this has to be sent to the WS for storing the data
		// for modularity purposes we shall have it in a different WS
		
		
        return "Success";
    }
	

	
	

	
	/**
	 * 
	 * 
	 * 
	 * @param callid
	 * @param idcaller 
	 * @param emo_annotations
	 * @param timestamp
	 */
	
	private void record_annotations(String callid, String idcaller, EmotionClass emo_annotations, long timestamp) {
		// TODO Auto-generated method stub
		
		//call the service(s) in which the annotation should be registered.
		//data base call here.
		
	}

	//
	private String record_file(String callid2, byte[] bs, String id, long timestamp) {
		// TODO Auto-generated method stub
		
		//if the call does not exist yet, we need to create the call. The callid is assumed to 
		//be provided by someone else !
		EmodashQueries qr= 	EmodashQueries.getEmodashQueryDb();
		String StreamId = UUID.randomUUID().toString();
		qr.insertVoice(StreamId, callid2,id, bs);
		
		String callid = "STUB"; // communication with the DB here.
		
		return callid;
	}

	/**
	 * Synchronous interaction with the annotation services.
	 * In a second architecture we could simply pass the DBs where to save the information
	 * to the annotators. 
	 * 
	 * A byte stream is given here that represent a wave file.
	 * 
	 * @param bs a by stream
	 * @return
	 */

	private EmotionClass get_annotations(String type, byte[] bs) {
		// TODO Auto-generated method stub
		
		//a list of annotators should be considered here, they should 
		//include machine learning annotators
		
		
		//so here we send the stuff to Guy ws.
		//create a rest call here you must send 
		RestTemplate template = new RestTemplate();
		
        JSONObject envelope = new JSONObject();
        envelope.append("data", bs);
        
        
		HttpHeaders headers = new HttpHeaders();
		headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

		MultiValueMap<String, String> map= new LinkedMultiValueMap<String, String>();
		map.add("data", envelope.toString());

		HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<MultiValueMap<String,String>>(map, headers);

		String getresString = template.postForObject( location_annotator+"/"+type, request , String.class );
        
        //String getresString = template.postForObject(location_annotator, request, String.class);
		System.err.println(getresString);

        JSONObject getres = new JSONObject(getresString);
        
        String[] predictionarr = getres.getJSONArray("predictions").toString().replace("[", "").replace("]", "").split(",");
        
        
        //Anger, Disgust,Fear... as below...
        EmotionClass emo= new EmotionClass(0,0,0,0,0,0,0);
        for(int i=0; i<predictionarr.length; i++){
        	
        	float f = Float.parseFloat(predictionarr[i]);
        	
        	if(i==0){
        		emo.setAnger(f);
        	}
        	if(i==1){	
        		emo.setDisgust(f);
        	}if(i==2){
        		
        		emo.setFear(f);
        	}if(i==3){
        		
        		
        		emo.setHappiness(f);
        	}if(i==4){
        		
        		emo.setNeutral(f);
        	}if(i==5){
        		
        		emo.setSadness(f);
        	}if(i==6){
        		
        		emo.setSurprise(f);
        	}
        	
        	
        }
        
        
        //System.out.println(prediction);
        //System.out.println(getres);
        
		return emo;
	}


	
	/**
	 * This method is meant to register all the DBs in which the speech samples have to be saved.
	 * @param dbaddress
	 * @return
	 */
	

	@PostMapping("/register_db_address")
	public String resiter_db_address(@RequestParam("db_address") String dbaddress){
		
		
		//To be persisted somewhere.
		//so that if the service goes down, it can retrieve it.
	
		
		try {
			PrintWriter out = new PrintWriter("databases.txt");
			out.append(dbaddress);
			out.flush();
			out.close();
			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	
		
		
		
		
		return "OK";
		
		//register here
		
	}
	
	/**
	 * 
	 * This method is meant to record the annotators associated with this service
	 * 
	 * @param annotator_address
	 * @return
	 */
	
	@PostMapping("/register_annotator_address")
	public String register_annotator_address(@RequestParam("annotator_address") String annotator_address){
		
		
		//To be persisted somewhere.
		//so that if the service goes down, it can retrieve it.
		try {
			PrintWriter out = new PrintWriter("annotators.txt");
			out.append(annotator_address);
			out.flush();
			out.close();
			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
		return "OK";
		
		//register here
		
	}
	
	

}
