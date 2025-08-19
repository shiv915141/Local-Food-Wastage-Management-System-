import sqlite3
import pandas as pd

def create_connection():
    """Create a database connection to a SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect('food_wastage.db')
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables(conn):
    """Create all necessary tables for the project."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS providers (
                Provider_ID INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                Type TEXT NOT NULL,
                Address TEXT NOT NULL,
                City TEXT NOT NULL,
                Contact TEXT NOT NULL
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS receivers (
                Receiver_ID INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                Type TEXT NOT NULL,
                City TEXT NOT NULL,
                Contact TEXT NOT NULL
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS food_listings (
                Food_ID INTEGER PRIMARY KEY,
                Food_Name TEXT NOT NULL,
                Quantity INTEGER NOT NULL,
                Expiry_Date DATE NOT NULL,
                Provider_ID INTEGER,
                Provider_Type TEXT NOT NULL,
                Location TEXT NOT NULL,
                Food_Type TEXT NOT NULL,
                Meal_Type TEXT NOT NULL,
                FOREIGN KEY (Provider_ID) REFERENCES providers (Provider_ID)
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS claims (
                Claim_ID INTEGER PRIMARY KEY,
                Food_ID INTEGER,
                Receiver_ID INTEGER,
                Status TEXT NOT NULL,
                Timestamp DATETIME NOT NULL,
                FOREIGN KEY (Food_ID) REFERENCES food_listings (Food_ID),
                FOREIGN KEY (Receiver_ID) REFERENCES receivers (Receiver_ID)
            );
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def load_data(conn):
    """Load data from CSV files into the database tables."""
    try:
        providers_df = pd.read_csv('providers_data.csv')
        receivers_df = pd.read_csv('receivers_data.csv')
        food_listings_df = pd.read_csv('food_listings_data.csv')
        claims_df = pd.read_csv('claims_data.csv')

        providers_df.to_sql('providers', conn, if_exists='replace', index=False)
        receivers_df.to_sql('receivers', conn, if_exists='replace', index=False)
        food_listings_df.to_sql('food_listings', conn, if_exists='replace', index=False)
        claims_df.to_sql('claims', conn, if_exists='replace', index=False)
    except Exception as e:
        print(f"Error loading data: {e}")

def get_data(conn, table_name, filters=None):
    """Retrieve data from a specified table with optional filters."""
    query = f"SELECT * FROM {table_name}"
    if filters:
        conditions = [f"{key} = '{value}'" for key, value in filters.items()]
        query += " WHERE " + " AND ".join(conditions)
    try:
        return pd.read_sql(query, conn)
    except pd.io.sql.DatabaseError as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()