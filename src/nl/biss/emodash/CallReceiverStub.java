package nl.biss.emodash;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.LinkedList;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@RestController
public class CallReceiverStub {
	
	
	@PostMapping("/post_wave_agent")
    public String AgentChannelProcessing(@RequestParam("file") MultipartFile file, @RequestParam("AgentID") String agentid) {

		//we shall pass through the annotation service, then store the file
		
		
		// ->
		//  annotate(file)
		
		//it should get a time stamp too, starting from here
		//for a matter of synch problems
		
		long timestamp = System.currentTimeMillis();
		
		LinkedList<String> list_of_annotations  = get_annotations(file); 
		//we need to accept the situation in which the annotations may fail. Each of the annotations
		//should be handled asynchronously
		//send it to the storing services
		String callid = record_file(file, agentid, timestamp);
		record_annotations(callid,list_of_annotations,timestamp); //this has to be sent to the WS for storing the data
		// for modularity purposes we shall have it in a different WS
		
		
        return "Success";
    }
	

	
	private void record_annotations(String callid, LinkedList<String> list_of_annotations, long timestamp) {
		// TODO Auto-generated method stub
		
		//call the service in which the annotation should be registered.
		
		
	}


	private String record_file(MultipartFile file, String agentid, long timestamp) {
		// TODO Auto-generated method stub
		
		String callid = "STUB"; // communication with the DB here.
		
		return callid;
	}

	/**
	 * Synchronous interaction with the annotation services.
	 * In a second architecture we could simply pass the DBs where to save the information
	 * to the annotators. 
	 * 
	 * @param file
	 * @return
	 */

	private LinkedList<String> get_annotations(MultipartFile file) {
		// TODO Auto-generated method stub
		
		//a list of annotators should be considered here, they should 
		//include machine learning annotators
		
		return null;
	}


	
	
	@PostMapping("/post_wave_customer")
    public String AgentChannelCustomer(@RequestParam("file") MultipartFile file, @RequestParam("AgentID") String agentid) {

		//we shall have a channel for the customer too.
		//here we expect a wav file of about 4 seconds.
		//same process as for the agent, but associated to the customer
		//ASSUMPTION: we know the customer id at this point in time.
		
		
        return "Success";
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
