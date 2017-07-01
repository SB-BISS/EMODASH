package nl.biss.emodash;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Date;

import com.mysql.jdbc.Connection;
import com.mysql.jdbc.PreparedStatement;
import com.mysql.jdbc.Statement;

public class EmodashQueries {
	
	private  String name = "EmoDashAdmin";
	private  String password = "emodash123";
	private  EmodashQueries singleton = null;
	private  Connection conn = null;
	
public EmodashQueries(){
	
	 String myDriver = "org.gjt.mm.mysql.Driver";
     String myUrl = "jdbc:mysql://localhost/emodash"; //assumpion is that we can find the DB in the local host
     //this assumption may change in the future
     
     try {
		Class.forName(myDriver);
		conn = (Connection) DriverManager.getConnection(myUrl, name, password);
	} catch (ClassNotFoundException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	} catch (SQLException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
     
	
}
	
/**
 * Singleton access to Database
 * 
 * @return
 */


//public static synchronized EmodashQueries getEmodashQueryDb(){
//	
//	EmodashQueries returnable = null;
//	
//	try {
//		if(singleton==null || conn.isClosed()){//semisingleton pattern
//			
//			returnable = new EmodashQueries();
//			
//		} else returnable = singleton;
//	} catch (SQLException e) {
//		// TODO Auto-generated catch block
//		e.printStackTrace();
//	}
//	
//	
//	return returnable;
//	
//}



public void connectionClose(){
	
	
	try {
		this.conn.close();
	} catch (SQLException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
}



/**
 * 
 * Helper method to insert a call in the database
 * 
 * @param CallId
 * @param AgentId
 * @param CustomerId
 */

public void insertCallId(String CallId, String AgentId, String CustomerId, long timestamp_beginning){
	
	String query= "Insert INTO phonecall (CallID, AgentID, CustomerID, timestamp_beginning) values ('"+CallId +"','"+AgentId + "','"+CustomerId+"'," + timestamp_beginning+")";
	
	try {
		Statement st = (Statement) conn.createStatement();
		
		st.execute(query);
		st.close();
		
	} catch (SQLException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
	
	
}



/**
 * 
 * Helper method to insert a call in the database
 * 
 * @param CallId
 * @param AgentId
 * @param CustomerId
 */

public void endCallId(String CallId, String AgentId, String CustomerId, long timestamp_end){
	
	String query= "Update phonecall set timestamp_end=" + timestamp_end +" where CustomerID='" + CustomerId + "' and CallId='"+CallId +"' and AgentId='"+AgentId + "';";
	
	try {
		Statement st = (Statement) conn.createStatement();
		
		st.execute(query);
		st.close();
		
	} catch (SQLException e) {
		// TODO Auto-generated catch block
		System.err.println(query);
		e.printStackTrace();
	}
	
	
}




public void insertVoice(String StreamId, String CallId,String PersonId, byte[] file){
	
	
	String sql = "INSERT INTO voicesignals (StreamId, CallId, PersonId, voice) values (?, ?, ?,?)";
    java.sql.PreparedStatement statement;
	try {
		statement = conn.prepareStatement(sql);
		InputStream inputStream = new ByteArrayInputStream(file);

		statement.setString(1,StreamId);
		statement.setString(2,CallId);
		statement.setString(3,PersonId);
		statement.setBlob(4, inputStream);
			
		statement.executeUpdate();
		statement.close();
		
	} catch (SQLException e) {
		// TODO Auto-generated catch block
		System.err.println("[INSERT VOICE]");
		e.printStackTrace();
	}
    
   
	
}


/**
 * This class queries the Emodash dataset
 * @param args
 */
public int emodashUpdate(String query){
 try
    {
      // create our mysql database connection
     
     

      // create the java statement
      Statement st = (Statement) conn.createStatement();
      
      // execute the query, and get a java resultset
      int rs = st.executeUpdate(query);
      
      // iterate through the java resultset
     
      st.close();
      return rs;
    }
    catch (Exception e)
    {
      e.printStackTrace();	
      System.err.println("Got an exception! " + query);
      System.err.println(e.getMessage());
    }
return 0;

}







	
	/**
	 * This class queries the Emodash dataset
	 * @param args
	 */
public ResultSet emodashQuery(String query){
	 try
	    {
	      // create our mysql database connection
	     
	     

	      // create the java statement
	      Statement st = (Statement) conn.createStatement();
	      
	      // execute the query, and get a java resultset
	      ResultSet rs = st.executeQuery(query);
	      
	      // iterate through the java resultset
	     
	      //st.close();
	      return rs;
	    }
	    catch (Exception e)
	    {
	      e.printStackTrace();	
	      System.err.println("Got an exception! " + query);
	      System.err.println(e.getMessage());
	    }
	return null;
	
}

public String clientQuery (String clientid){
	
	String clientQuery= "SELECT * FROM customer Where ID ="+clientid;;
	ResultSet rs=emodashQuery(clientQuery);
	
	 try {
		while (rs.next())
		 {
		
		   int id = rs.getInt("id");
		   String firstName = rs.getString("first_name");
		   String lastName = rs.getString("last_name");
		   Date dateCreated = rs.getDate("date_created");
		   boolean isAdmin = rs.getBoolean("is_admin");
		   int numPoints = rs.getInt("num_points");
		   
		   // print the results
		   System.out.format("%s, %s, %s, %s, %s, %s\n", id, firstName, lastName, dateCreated, isAdmin, numPoints);
		 }
	} catch (SQLException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
	return null;
	
}


}