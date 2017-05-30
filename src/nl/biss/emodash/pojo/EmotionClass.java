package nl.biss.emodash.pojo;

public class EmotionClass {

	
	float sadness;
	float happiness;
	float neutral;
	float fear;
	float disgust;
	float anger;
	float surprise;
	
	
	public EmotionClass(float anger, float disgust, float fear, float happiness, float neutral, float sadness, float surprise){
		
		
		this.anger= anger;
		this.disgust= disgust;
		this.fear= fear;
		this.happiness=happiness;
		this.neutral= neutral;
		this.sadness = sadness;
		this.surprise = surprise;
		
	}
	
	
	
	
	public float getSadness() {
		return sadness;
	}
	public void setSadness(float sadness) {
		this.sadness = sadness;
	}
	public float getHappiness() {
		return happiness;
	}
	public void setHappiness(float happiness) {
		this.happiness = happiness;
	}
	public float getNeutral() {
		return neutral;
	}
	public void setNeutral(float neutral) {
		this.neutral = neutral;
	}
	public float getFear() {
		return fear;
	}
	public void setFear(float fear) {
		this.fear = fear;
	}
	public float getDisgust() {
		return disgust;
	}
	public void setDisgust(float disgust) {
		this.disgust = disgust;
	}
	public float getAnger() {
		return anger;
	}
	public void setAnger(float anger) {
		this.anger = anger;
	}
	public float getSurprise() {
		return surprise;
	}
	public void setSurprise(float surprise) {
		this.surprise = surprise;
	}
	
	
	
	
	
}
