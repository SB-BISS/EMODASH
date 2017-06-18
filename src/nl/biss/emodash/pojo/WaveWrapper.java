package nl.biss.emodash.pojo;

import java.io.Serializable;

//Pojo for byte stream to simplify the handling of 
//the files. Get the object and save the byte stream as a wav file if you want
//to play it.

public class WaveWrapper implements Serializable{
	
	byte[] wav_stream;
	private String id;
	//for a real environment, this probably is one id for the caller and customer.
	//we need to see what is the current situation in the stakeholders and define
	//adapters.
	private String callid;
	
	
	public WaveWrapper(){
		super();
	}
	
	
	
	public byte[] getWav_stream() {
		return wav_stream;
	}

	public void setWav_stream(byte[] wav_stream) {
		this.wav_stream = wav_stream;
	}

	public String getId() {
		// TODO Auto-generated method stub
		return id;
	}
	
	public void setId(String id){
		
		this.id=id;
	}

	public String getCallId() {
		// TODO Auto-generated method stub
		return null;
	}
	
	
	
	
	

}
