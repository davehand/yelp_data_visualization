package yelpReviews;

import java.sql.*;

public class YelpReviews {

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
		
		try {
			// Establish a connection and create a statement
			connection = DriverManager.getConnection(url, username, password);
			statement = connection.createStatement();
			
			// Query the DB to find out the total number of businesses
			String query = "SELECT COUNT(*) AS num_businesses " +
						   "FROM BUSINESS";
			result = statement.executeQuery(query);
			
			result.next();
			int numBusinesses = Integer.parseInt(result.getString("num_businesses"));
			
			String[] insertions = new String[numBusinesses];
			
			// Execute the query for all reviews
			query = "SELECT business_id, stars, useful_votes " +
						   "FROM review " +
						   "ORDER BY business_id";
			result = statement.executeQuery(query);
			
			boolean resultsRemaining = result.next();
			int index = 0;
			
			while (resultsRemaining) {
				
				int totalVotes = 0;
				int totalScore = 0;
				String currentID = result.getString("business_id");
				
				// Query results are ordered by business_id, so we iterate through
				// all of a business's reviews consecutively
				while (result.getString("business_id").equals(currentID)) {
					int votes = Integer.parseInt(result.getString("useful_votes")) + 1;
					int stars = Integer.parseInt(result.getString("stars"));
					totalVotes += votes;
					totalScore += votes * stars;
					
					if (!result.next()) {
						resultsRemaining = false;
						break;
					}
				}
				
				// Calculate the average rating for each business
				double avgScore = (double) totalScore / totalVotes;
				String avgRating = avgScore + "";
				if (avgRating.length() > 5) {
					avgRating = avgRating.substring(0, 5);
				}
				
				// Store the corresponding INSERT statement in an array
				String insertion = "INSERT INTO business_rating VALUES ('" + currentID + "', " + avgRating + ")";
				insertions[index] = insertion;
				
				if (index % (numBusinesses / 1000) == 0) {
					System.out.println(currentID + "\t" + totalVotes + "\t" + avgRating);
				}
				index++;
			}
			
			// Execute all of the INSERT statements
			for (int i = 0; i < insertions.length; i++) {
				if (insertions[i] != null) {
					if (i % (numBusinesses / 1000) == 0) {
						System.out.println(insertions[i]);
					}
					statement.execute(insertions[i]);
				}
			}
			
			// Close the connections
			result.close();
			statement.close();
			connection.close();
			
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
}
