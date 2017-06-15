package nl.biss.emodash.pojo;

import java.io.Serializable;

public class AnagraphicData implements Serializable{

	

	    private String name;
	    private int age;
	    private String gender;
	    private String surname;
	    private String adress;

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
			this.adress=adress;
		}
		
		
		
		public String getSurname() {
			return surname;
		}
		public String getAdress() {
			return adress;
		}
		public void setSurname(String surname) {
			// TODO Auto-generated method stub
			this.surname= surname;
		}

	
}
