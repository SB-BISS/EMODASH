package nl.biss.emodash;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Properties;

public class DataBase {

	/**
	 * This class creates the Emodash Database
	 * @param args
	 */
	protected DataBase() {
		    String name = "emodash";
            String user = "EmoDashAdmin";
            String password = "emodash123";
            
			//createDB(name, user, password);
			Connection con=connectDB(name, user, password);
			System.err.println(con.toString());
			
			//Defining the DB Schema
			String mysql= "CREATE TABLE `EMOTIONS` ( `StreamID` varchar(45) NOT NULL,`CallID` varchar(45) NOT NULL,  `EmotionType` varchar(45) NOT NULL,`Value` float NOT NULL, 'Timestamp' BIGINT NOT NULL, PRIMARY KEY (`StreamID`,`CallID`))";
			String mysql1= "CREATE TABLE `Customer` (`CustomerID` varchar(45) NOT NULL,`Name` varchar(45) NOT NULL,`Surname` varchar(45) NOT NULL,`Age` varchar(45) DEFAULT NULL,`Sex` varchar(45) DEFAULT NULL,`Adress` varchar(45) DEFAULT NULL,`Region` varchar(45) DEFAULT NULL, PRIMARY KEY (`CustomerID`))";
			String mysql2= "CREATE TABLE `Emotion_history` ( `CustomerID` varchar(45) NOT NULL, `CallID` varchar(45) NOT NULL,`Emotion_anger` varchar(45) NOT NULL,`Emotion_disgust` varchar(45) NOT NULL,`Emotion_fear` varchar(45) NOT NULL,`Emotion_happiness` varchar(45) NOT NULL,`Emotion_neutral` varchar(45) NOT NULL,`Emotion_sadness` varchar(45) NOT NULL, PRIMARY KEY (`CustomerID`,`CallID`))";
			String mysql3= "CREATE TABLE `PhoneCall` (`CallID` varchar(45) NOT NULL,`CustomerID` varchar(45) NOT NULL,`AgentID` varchar(45) NOT NULL,'Timestamp_beginning' BIGINT NOT NULL, PRIMARY KEY (`CallID`))";
			String mysql4= "CREATE TABLE `VoiceSignals` (`StreamID` varchar(45) NOT NULL, `CallID` varchar(45) NOT NULL, PRIMARY KEY (`StreamID`))";
			
			//Creating the tables
			createDBTable(con,mysql);
			createDBTable(con,mysql1);
			createDBTable(con,mysql2);
			createDBTable(con,mysql3);
			createDBTable(con,mysql4);   

}
		/*CREATES EMODASH DB!*/
		protected boolean createDB(String name, String user, String password){
			
			 // JDBC driver name and database URL
			  // private String JDBC_DRIVER = "com.mysql.jdbc.Driver";  
			   String DB_URL = "jdbc:mysql://localhost/";
			   Connection conn = null;
			   Statement stmt = null;
			   
			   try{
			      //STEP 2: Register JDBC driver
			      Class.forName("com.mysql.jdbc.Driver");

			      //STEP 3: Open a connection
			      System.out.println("Connecting to database...");
			      conn = DriverManager.getConnection(DB_URL, user, password);

			      //STEP 4: Execute a query
			      System.out.println("Creating database...");
			      stmt = conn.createStatement();
			      
			      String sql = "CREATE DATABASE "+name;
			      stmt.executeUpdate(sql);
			      System.out.println("Database created successfully...");
			   }catch(SQLException se){
			      //Handle errors for JDBC
			      se.printStackTrace();
			   }catch(Exception e){
			      //Handle errors for Class.forName
			      e.printStackTrace();
			   }finally{
			      //finally block used to close resources
			      try{
			         if(stmt!=null)
			            stmt.close();
			      }catch(SQLException se2){
			      }// nothing we can do
			      try{
			         if(conn!=null)
			            conn.close();
			      }catch(SQLException se){
			         se.printStackTrace();
			      }//end finally try
			   }//end try
			   System.out.println("If there was an excption, maybe the DB exists alredy!");
			return true;
		}
		
		/*CONNECTS TO EMODASH!*/
		protected Connection  connectDB(String name, String user, String password){
			
			boolean connected=false;
			/*
			 * 3 possible connection links
			 * */
			Connection conn1 = null;
	        Connection conn2 = null;
	        Connection conn3 = null;
	        if(connected==false){
	        try {
	            String url1 = "jdbc:mysql://localhost:3306/"+name;
	         
	            conn1 = DriverManager.getConnection(url1, user, password);
	            if (conn1 != null){
	                System.out.println("Connected to the database test1");
	                connected=true;
	            	return conn1;
	            	}
	            String url2 = "jdbc:mysql://localhost:3306/emodash?user="+name+"&password="+password;
	            conn2 = DriverManager.getConnection(url2);
	            if (conn2 != null) {
	                System.out.println("Connected to the database test2");
	                connected=true;
	            	return conn2;
	            }

	            String url3 = "jdbc:mysql://localhost:3306/"+name;
	            Properties info = new Properties();
	            info.put("user", user);
	            info.put("password", password);

	            conn3 = DriverManager.getConnection(url3, info);
	            if (conn3 != null) {
	                System.out.println("Connected to the database test3");
	                connected=true;
	                return conn3;
	            }
	            }
	        catch (SQLException ex) {
	            System.out.println("An error occurred. Maybe user/password is invalid");
	            ex.printStackTrace();
	            connected=false;
	            return null;
	        }
	        }
			//return true;
	       
			return null;
			
		}

	protected boolean createDBTable(Connection con,String myTable){
		 try{
		   Statement stmt = con.createStatement();

		   stmt.executeUpdate(myTable);
		   System.out.println("TABLE created successfully...");
		   return true;
	   }catch(SQLException se){
		   
	      //Handle errors for JDBC
	      se.printStackTrace();
		return false;
		}
		
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		DataBase db=new DataBase();
		 
	}
}