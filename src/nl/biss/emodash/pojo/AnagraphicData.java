package nl.biss.emodash.pojo;

import java.io.Serializable;

public class AnagraphicData implements Serializable{

	

	    private String name;
	    private int age;
	    private String gender;
	    private String surname;
	    private String address;
	    private String region;
		private String postal_code;

	    public String getGender() {
			return gender;
		}
		public void setGender(String gender) {
			this.gender = gender;
		}
		public String getName() { return this.name; }
	    public void setName( String name ) { this.name = name; }

	    public Integer getAge() { return this.age; }
	    public void setAge( int age ) { this.age = age; }
	    
		public void setAdress(String adress) {
			// TODO Auto-generated method stub
			this.address=adress;
		}
		
		
		
		public String getAddress() {
			return address;
		}
		public void setAddress(String address) {
			this.address = address;
		}
		public String getRegion() {
			return region;
		}
		public void setRegion(String region) {
			this.region = region;
		}
		public String getSurname() {
			return surname;
		}
	
		public void setSurname(String surname) {
			// TODO Auto-generated method stub
			this.surname= surname;
		}
		public void setPostalCode(String postal_code) {
			// TODO Auto-generated method stub
			this.postal_code = postal_code;
		}
		
		public String getPostalCode(){
			return this.postal_code;
		}
	
}
