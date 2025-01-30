import pandas as pd
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the database connection details from environment variables
db_name = os.getenv('POSTGRES_DATABASE')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('DATABASE_HOST', 'localhost')
db_port = os.getenv('DATABASE_PORT', '5432')

# Storing CSV file into a dataframe
file_path = 'data/RTE-Annuel-Definitif-2022.csv'

# Load the CSV
df = pd.read_csv(file_path)

# Select only relevant columns and handle missing data
df = df[['Date', 'Heures', 'Consommation']]
df['Consommation'] = pd.to_numeric(df['Consommation'], errors='coerce')

# Remove rows where 'Consommation' is NaN
df = df.dropna(subset=['Consommation'])

# Remove rows where the 'Date' is NaN
df = df.dropna(subset=['Date'])

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)

# Create a cursor to execute queries
cur = conn.cursor()

# Drop the table if it exists
cur.execute("DROP TABLE IF EXISTS consommation;")

# Create the table
create_table_query = """
CREATE TABLE consommation (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    heures TIME NOT NULL,
    puissance DECIMAL(10, 2) NOT NULL
);
"""
cur.execute(create_table_query)

# Insert data into the database
for index, row in df.iterrows():
    if pd.notna(row['Consommation']):
        cur.execute(
            sql.SQL("INSERT INTO consommation (date, heures, puissance) VALUES (%s, %s, %s)"),
            [row['Date'], row['Heures'], row['Consommation']]
        )

# Commit and close the connection
conn.commit()
cur.close()
conn.close()

print("Data inserted successfully!")