package nl.biss.emodash;

import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Date;

import com.mysql.jdbc.Connection;
import com.mysql.jdbc.Statement;

public class EmodashQueries {
	/**
	 * This class queries the Emodash dataset
	 * @param args
	 */
public ResultSet emodashQuery(String query){
	 try
	    {
	      // create our mysql database connection
	      String myDriver = "org.gjt.mm.mysql.Driver";
	      String myUrl = "jdbc:mysql://localhost/emodash";
	      Class.forName(myDriver);
	      Connection conn = (Connection) DriverManager.getConnection(myUrl, "visara", "Emodash.123");
	     

	      // create the java statement
	      Statement st = (Statement) conn.createStatement();
	      
	      // execute the query, and get a java resultset
	      ResultSet rs = st.executeQuery(query);
	      
	      // iterate through the java resultset
	     
	     
	      st.close();
	      return rs;
	    }
	    catch (Exception e)
	    {
	      System.err.println("Got an exception! ");
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