#---    Imports    ---#
import	pandas as pd
import	psycopg2
from	psycopg2 import sql
from	dotenv import load_dotenv
from	app import DEBUG
import	os

# Load environment variables from .env file
load_dotenv()

# Get the database connection details from environment variables
db_name = os.getenv('POSTGRES_DATABASE')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('DATABASE_HOST', 'localhost')
db_port = os.getenv('DATABASE_PORT', '5432')

# Storing into a dataframe
file_path = '../data/RTE-Annuel-Definitif-2022.csv'
df = pd.read_csv(file_path)

# Select only the relevant columns
df = df[['Date', 'Consommation']]

# Ensure Consommation is a numeric value and handle missing data (set to None or 0)
df['Consommation'] = pd.to_numeric(df['Consommation'], errors='coerce')


if DEBUG == True:
	print("First 5 rows of the CSV file:")
	print(df.head())

# Connecting to the PostgreSQL database
conn = psycopg2.connect(
	dbname=db_name, 
	user=db_user, 
	password=db_password, 
	host=db_host, 
	port=db_port
)

# Creating cursor to execute queries
cur = conn.cursor()

# Inserting data into the database
for index, row in df.iterrows():
    if pd.notna(row['Consommation']):  # Only insert rows where consumption is not NaN
        cur.execute(
            sql.SQL("INSERT INTO consumption_data (timestamp, consumption) VALUES (%s, %s)"),
            [row['Date'], row['Consommation']]
        )

# Commit and close the connection
conn.commit()
cur.close()
conn.close()

print("Données insérées avec succès!")
