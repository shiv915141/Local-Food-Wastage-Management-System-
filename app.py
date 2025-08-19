import streamlit as st
import pandas as pd
import sqlite3
from database_manager import create_connection, create_tables, load_data, get_data
from data_analysis import *

def main():
    st.set_page_config(layout="wide")
    st.title("Local Food Wastage Management System 🍎♻️")

    conn = create_connection()
    if conn:
        try:
            create_tables(conn)
            load_data(conn)
        except Exception as e:
            st.error(f"Failed to connect or load data: {e}")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Detailed Analysis", "Food Listings", "Provider Actions", "SQL Query Runner"])

    if page == "Dashboard":
        st.header("Analytics Dashboard")
        st.subheader("Key Metrics at a Glance")

        col1, col2, col3 = st.columns(3)
        
        total_food_df = total_food_available(conn)
        total_food = total_food_df.iloc[0]['Total_Available_Food'] if not total_food_df.empty else 0
        with col1:
            st.metric("Total Food Available (Units)", f"{total_food:,}")
            
        total_providers = run_query(conn, "SELECT COUNT(*) FROM providers").iloc[0, 0]
        with col2:
            st.metric("Total Food Providers", f"{total_providers:,}")
            
        total_receivers = run_query(conn, "SELECT COUNT(*) FROM receivers").iloc[0, 0]
        with col3:
            st.metric("Total Receivers", f"{total_receivers:,}")

        st.markdown("---")
        
        st.subheader("High-Impact Insights")
        
        # Display the most claimed meal type as a clear metric or chart
        most_claimed_df = most_claimed_meal_type(conn)
        if not most_claimed_df.empty:
            most_claimed_meal = most_claimed_df.iloc[0]['Meal_Type']
            most_claimed_count = most_claimed_df.iloc[0]['Total_Claims']
            st.info(f"The most claimed meal type is **{most_claimed_meal}** with **{most_claimed_count}** claims.")

        # You can also add charts here for visualization, e.g.,
        # st.bar_chart(most_common_food_types(conn).set_index('Food_Type'))
        
    elif page == "Detailed Analysis":
        st.header("Comprehensive Data Analysis")
        st.markdown("Here you can find detailed reports and all 15 key insights from the project.")

        st.subheader("Providers & Receivers")
        st.write("1. Providers and Receivers per City:")
        st.dataframe(providers_receivers_per_city(conn))
        st.write("2. Most Contributing Provider Type:")
        st.dataframe(most_contributing_provider_type(conn))
        st.write("3. Receivers with Most Food Claimed:")
        st.dataframe(top_receivers(conn))
        st.write("4. What is the total quantity of food donated by each provider?")
        st.dataframe(total_donated_by_provider(conn))
        
        st.markdown("---")
        
        st.subheader("Listings & Availability")
        st.write("5. Total Quantity of Available Food:")
        st.dataframe(total_food_available(conn))
        st.write("6. City with Highest Number of Food Listings:")
        st.dataframe(city_with_most_listings(conn))
        st.write("7. Most Commonly Available Food Types:")
        st.dataframe(most_common_food_types(conn))
        st.write("8. Food Listings by Expiry Date:")
        st.dataframe(listings_by_expiry_date(conn))

        st.markdown("---")

        st.subheader("Claims & Distribution")
        st.write("9. Claims per Food Item:")
        st.dataframe(claims_per_food_item(conn))
        st.write("10. Top Provider by Successful Claims:")
        st.dataframe(top_provider_by_successful_claims(conn))
        st.write("11. Claim Status Percentages:")
        st.dataframe(claim_status_percentages(conn))
        st.write("12. Average Quantity of Food Claimed per Receiver:")
        st.dataframe(avg_food_claimed_per_receiver(conn))
        st.write("13. Most Claimed Meal Type:")
        st.dataframe(most_claimed_meal_type(conn))
        st.write("14. Unclaimed Food Items:")
        st.dataframe(unclaimed_food_items(conn))
        
        st.markdown("---")

    elif page == "Food Listings":
        # ... (rest of the code for Food Listings page)
        st.header("Available Food Listings")
        all_listings = get_data(conn, 'food_listings')
        all_cities = sorted(all_listings['Location'].unique())
        all_provider_types = sorted(all_listings['Provider_Type'].unique())
        all_food_types = sorted(all_listings['Food_Type'].unique())
        
        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            city_filter = st.multiselect("Filter by City", all_cities)
        with col2:
            provider_type_filter = st.multiselect("Filter by Provider Type", all_provider_types)
        with col3:
            food_type_filter = st.multiselect("Filter by Food Type", all_food_types)

        search_query = st.text_input("Search for a food item (e.g., 'Pizza', 'Salad')", "")
        st.markdown("---")

        filtered_df = all_listings.copy()
        if city_filter:
            filtered_df = filtered_df[filtered_df['Location'].isin(city_filter)]
        if provider_type_filter:
            filtered_df = filtered_df[filtered_df['Provider_Type'].isin(provider_type_filter)]
        if food_type_filter:
            filtered_df = filtered_df[filtered_df['Food_Type'].isin(food_type_filter)]
        if search_query:
            filtered_df = filtered_df[filtered_df['Food_Name'].str.contains(search_query, case=False)]

        st.subheader(f"Showing {len(filtered_df)} available listings")
        
        num_cols = 3 
        cols = st.columns(num_cols)
        
        for index, row in filtered_df.iterrows():
            col = cols[index % num_cols]
            with col:
                with st.container(border=True):
                    st.markdown(f"**{row['Food_Name']}**")
                    st.write(f"**Quantity:** {row['Quantity']} units")
                    st.write(f"**Location:** {row['Location']}")
                    st.write(f"**Expires:** {row['Expiry_Date']}")
                    
                    with st.expander("More Details"):
                        provider_name_query = f"SELECT Name, Contact, Address FROM providers WHERE Provider_ID = {row['Provider_ID']}"
                        provider_details = run_query(conn, provider_name_query)
                        if not provider_details.empty:
                            provider_name = provider_details.iloc[0]['Name']
                            provider_contact = provider_details.iloc[0]['Contact']
                            provider_address = provider_details.iloc[0]['Address']
                            st.write(f"**Provided by:** {provider_name}")
                            st.write(f"**Contact:** {provider_contact}")
                            st.write(f"**Address:** {provider_address}")
                        st.write(f"**Food Type:** {row['Food_Type']}")
                        st.write(f"**Meal Type:** {row['Meal_Type']}")
        
        if filtered_df.empty:
            st.warning("No listings match your filter criteria. Please adjust your selections.")

    elif page == "Provider Actions":
        # ... (rest of the code for Provider Actions page)
        st.header("Provider CRUD Operations")
        
        tab1, tab2, tab3 = st.tabs(["Add Listing", "Update Listing", "Delete Listing"])
        
        with tab1:
            st.subheader("Add a New Food Listing")
            with st.form("add_listing_form"):
                provider_id = st.number_input("Provider ID", min_value=1, step=1)
                food_name = st.text_input("Food Name")
                quantity = st.number_input("Quantity", min_value=1, step=1)
                expiry_date = st.date_input("Expiry Date")
                provider_type = st.selectbox("Provider Type", ["Restaurant", "Grocery Store", "Supermarket"])
                location = st.text_input("Location (City)")
                food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
                meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
                
                submitted = st.form_submit_button("Add Listing")
                if submitted:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("INSERT INTO food_listings (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                                       (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type))
                        conn.commit()
                        st.success("Listing added successfully!")
                    except sqlite3.Error as e:
                        st.error(f"Error adding listing: {e}")
        
        with tab2:
            st.subheader("Update an Existing Listing")
            listing_id_to_update = st.number_input("Enter Food ID to update", min_value=1)
            with st.form("update_listing_form"):
                new_quantity = st.number_input("New Quantity", min_value=1, step=1)
                update_submitted = st.form_submit_button("Update Listing")
                if update_submitted:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("UPDATE food_listings SET Quantity = ? WHERE Food_ID = ?", (new_quantity, listing_id_to_update))
                        conn.commit()
                        st.success(f"Listing {listing_id_to_update} updated successfully!")
                    except sqlite3.Error as e:
                        st.error(f"Error updating listing: {e}")

        with tab3:
            st.subheader("Delete a Food Listing")
            listing_id_to_delete = st.number_input("Enter Food ID to delete", min_value=1, key='delete_input')
            delete_submitted = st.button("Delete Listing", key='delete_button')
            if delete_submitted:
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM food_listings WHERE Food_ID = ?", (listing_id_to_delete,))
                    conn.commit()
                    st.success(f"Listing {listing_id_to_delete} deleted successfully!")
                except sqlite3.Error as e:
                    st.error(f"Error deleting listing: {e}")

    elif page == "SQL Query Runner":
        st.header("Manual SQL Query Runner 🚀")
        st.warning("⚠️ This feature allows you to run custom SQL commands. Use it for authorized administrative tasks only.")
        
        query = st.text_area("Enter your SQL query here:", height=200, help="e.g., SELECT * FROM food_listings WHERE Quantity > 50;")
        
        if st.button("Run Query"):
            if query:
                try:
                    result_df = run_query(conn, query)
                    if not result_df.empty:
                        st.success("Query executed successfully!")
                        st.dataframe(result_df)
                        
                        csv_data = result_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Data as CSV",
                            data=csv_data,
                            file_name="query_results.csv",
                            mime="text/csv",
                        )
                    else:
                        st.info("Query executed successfully, but no results were returned.")
                except pd.io.sql.DatabaseError as e:
                    st.error(f"SQL Error: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
            else:
                st.warning("Please enter a query to run.")

if __name__ == "__main__":
    main()