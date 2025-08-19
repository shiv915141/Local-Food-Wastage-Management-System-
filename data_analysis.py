import pandas as pd

def run_query(conn, query, params=None):
    """A helper function to run an SQL query and return a DataFrame."""
    try:
        return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        print(f"Error running query: {e}")
        return pd.DataFrame()

# 1. How many food providers and receivers are there in each city?
def providers_receivers_per_city(conn):
    query = """
    SELECT
        City,
        SUM(CASE WHEN Type IN ('Restaurant', 'Grocery Store', 'Supermarket') THEN 1 ELSE 0 END) AS Providers_Count,
        SUM(CASE WHEN Type IN ('NGO', 'Community Center', 'Individual') THEN 1 ELSE 0 END) AS Receivers_Count
    FROM (
        SELECT City, Type FROM providers
        UNION ALL
        SELECT City, Type FROM receivers
    )
    GROUP BY City
    ORDER BY City;
    """
    return run_query(conn, query)

# 2. Which type of food provider contributes the most food?
def most_contributing_provider_type(conn):
    query = """
    SELECT 
        p.Type,
        SUM(fl.Quantity) AS Total_Quantity
    FROM providers p
    JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID
    GROUP BY p.Type
    ORDER BY Total_Quantity DESC
    LIMIT 1;
    """
    return run_query(conn, query)

# 3. What is the contact information of food providers in a specific city?
def provider_contacts_by_city(conn, city):
    query = """
    SELECT 
        Name,
        Contact,
        Address
    FROM providers
    WHERE City = ?;
    """
    return run_query(conn, query, params=(city,))

# 4. Which receivers have claimed the most food?
def top_receivers(conn):
    query = """
    SELECT 
        r.Name,
        SUM(fl.Quantity) AS Total_Food_Claimed
    FROM receivers r
    JOIN claims c ON r.Receiver_ID = c.Receiver_ID
    JOIN food_listings fl ON c.Food_ID = fl.Food_ID
    WHERE c.Status = 'Completed'
    GROUP BY r.Name
    ORDER BY Total_Food_Claimed DESC;
    """
    return run_query(conn, query)

# 5. What is the total quantity of food available from all providers?
def total_food_available(conn):
    query = """
    SELECT 
        SUM(Quantity) AS Total_Available_Food
    FROM food_listings;
    """
    return run_query(conn, query)

# 6. Which city has the highest number of food listings?
def city_with_most_listings(conn):
    query = """
    SELECT 
        Location,
        COUNT(Food_ID) AS Number_of_Listings
    FROM food_listings
    GROUP BY Location
    ORDER BY Number_of_Listings DESC
    LIMIT 1;
    """
    return run_query(conn, query)

# 7. What are the most commonly available food types?
def most_common_food_types(conn):
    query = """
    SELECT 
        Food_Type,
        COUNT(Food_ID) AS Number_of_Listings
    FROM food_listings
    GROUP BY Food_Type
    ORDER BY Number_of_Listings DESC;
    """
    return run_query(conn, query)

# 8. How many food claims have been made for each food item?
def claims_per_food_item(conn):
    query = """
    SELECT 
        fl.Food_Name,
        COUNT(c.Claim_ID) AS Number_of_Claims
    FROM food_listings fl
    LEFT JOIN claims c ON fl.Food_ID = c.Food_ID
    GROUP BY fl.Food_Name
    ORDER BY Number_of_Claims DESC;
    """
    return run_query(conn, query)

# 9. Which provider has had the highest number of successful food claims?
def top_provider_by_successful_claims(conn):
    query = """
    SELECT 
        p.Name,
        COUNT(c.Claim_ID) AS Successful_Claims_Count
    FROM providers p
    JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID
    JOIN claims c ON fl.Food_ID = c.Food_ID
    WHERE c.Status = 'Completed'
    GROUP BY p.Name
    ORDER BY Successful_Claims_Count DESC
    LIMIT 1;
    """
    return run_query(conn, query)

# 10. What percentage of food claims are completed vs. pending vs. canceled?
def claim_status_percentages(conn):
    query = """
    SELECT
        Status,
        COUNT(Claim_ID) * 100.0 / (SELECT COUNT(*) FROM claims) AS Percentage
    FROM claims
    GROUP BY Status;
    """
    return run_query(conn, query)

# 11. What is the average quantity of food claimed per receiver?
def avg_food_claimed_per_receiver(conn):
    query = """
    SELECT 
        AVG(Total_Claimed) AS Average_Quantity_Per_Receiver
    FROM (
        SELECT 
            Receiver_ID,
            SUM(fl.Quantity) AS Total_Claimed
        FROM claims c
        JOIN food_listings fl ON c.Food_ID = fl.Food_ID
        WHERE c.Status = 'Completed'
        GROUP BY Receiver_ID
    );
    """
    return run_query(conn, query)

# 12. Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?
def most_claimed_meal_type(conn):
    query = """
    SELECT 
        fl.Meal_Type,
        COUNT(c.Claim_ID) AS Total_Claims
    FROM food_listings fl
    JOIN claims c ON fl.Food_ID = c.Food_ID
    GROUP BY fl.Meal_Type
    ORDER BY Total_Claims DESC
    LIMIT 1;
    """
    return run_query(conn, query)

# 13. What is the total quantity of food donated by each provider?
def total_donated_by_provider(conn):
    query = """
    SELECT 
        p.Name,
        SUM(fl.Quantity) AS Total_Quantity_Donated
    FROM providers p
    JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID
    GROUP BY p.Name
    ORDER BY Total_Quantity_Donated DESC;
    """
    return run_query(conn, query)

# 14. Which food items have not been claimed at all?
def unclaimed_food_items(conn):
    query = """
    SELECT 
        fl.Food_Name,
        fl.Provider_Type,
        fl.Location
    FROM food_listings fl
    LEFT JOIN claims c ON fl.Food_ID = c.Food_ID
    WHERE c.Claim_ID IS NULL;
    """
    return run_query(conn, query)

# 15. What is the distribution of food listings by expiry date (e.g., how many listings expire in the next 7 days)?
def listings_by_expiry_date(conn):
    query = """
    SELECT 
        CASE
            WHEN Expiry_Date <= date('now', '+7 days') THEN 'Expiring in < 7 days'
            WHEN Expiry_Date > date('now', '+7 days') AND Expiry_Date <= date('now', '+30 days') THEN 'Expiring in 7-30 days'
            ELSE 'Expiring in > 30 days'
        END AS Expiry_Category,
        COUNT(Food_ID) AS Number_of_Listings
    FROM food_listings
    GROUP BY Expiry_Category;
    """
    return run_query(conn, query)