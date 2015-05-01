package yelpReviews;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;

public class Benchmarking {

	public static void main(String[] args) {
		// Load the driver
		try {
			Class.forName("oracle.jdbc.driver.OracleDriver");
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		}

		String url = "jdbc:oracle:thin:damn@//yelp.czscqrbdzjc7.us-east-1.rds.amazonaws.com:1521/ouryelp";
		String username = "damn";
		String password = "damnyelp";

		Connection connection;
		Statement statement;
		ResultSet result;
		ResultSetMetaData resultMetaData;
		
		int numTrials = 500;
		long startTime = System.currentTimeMillis();

		for (int i = 0; i < numTrials; i++) {
			
			try {
				// Establish a connection and create a statement
				connection = DriverManager.getConnection(url, username, password);
				statement = connection.createStatement();
	
				String query = "WITH aggregate_scores_votes AS\n" +
							   "(\n"
							   	+ "SELECT business_id, sum(stars * (useful_votes + 1)) AS total_score, sum(useful_votes + 1) as total_votes\n"
							   	+ "FROM review\n"
							   	+ "GROUP BY business_id\n"
							 + "),\n"
							 + "avg_business_rating AS\n"
							 + "(\n"
							 	+ "SELECT business_id, (total_score/total_votes) as avg_rating\n"
							 	+ "FROM aggregate_scores_votes\n"
							 + ")\n"
							 + "SELECT avg_rating, latitude, longitude\n"
							 + "FROM business, avg_business_rating\n"
							 + "WHERE business.business_id = avg_business_rating.business_id\n"
							 	+ "AND business.NAME = 'McDonald''s'\n";
				
				result = statement.executeQuery(query);
	
				//Uncomment to check results 
	//			while (result.next()) {
	//				System.out.println(result.getString(1) + ",  " + result.getString(2) + ",  " + result.getString(3));
	//			}
				
				// Close the connections
				result.close();
				statement.close();
				connection.close();
				
				System.out.println("Finished trial #" + i);
	
			} catch (SQLException e) {
				e.printStackTrace();
			}
			
		}

		long stopTime = System.currentTimeMillis();
		
		System.out.println("Average query execution time: " + (stopTime - startTime)/numTrials + " milliseconds");
		
	}

}
