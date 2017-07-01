package nl.biss.emodash.pojo;

import java.io.Serializable;

public class SingleEmotion implements Serializable{
	
	private String Emotiontype;
	private float value = 0.0f;
	
	
	public SingleEmotion(String Emotiontype, float value){
		
		this.Emotiontype = Emotiontype;
		this.value = value;
	}


	public String getEmotiontype() {
		return Emotiontype;
	}


	public void setEmotiontype(String emotiontype) {
		Emotiontype = emotiontype;
	}


	public float getValue() {
		return value;
	}


	public void setValue(float value) {
		this.value = value;
	}
	
	
	

}
