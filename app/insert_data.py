#---	Imports		---#
import  pandas as pd
import  psycopg2
from    psycopg2 import sql

# Storing into a dataframe
file_path = '../data/RTE-Annuel-Definitif-2022.csv'
df = pd.read_csv(file_path)

# Connecting to the PostgreSQL database
conn = psycopg2.connect(
	dbname="your_db_name", 
	user="your_db_user", 
	password="your_db_password", 
	host="localhost", 
	port="5432"
)

# Creating cursor to execute queries
cur = conn.cursor()

# Inserting data into the database
for index, row in df.iterrows():
	cur.execute(
		sql.SQL("INSERT INTO consommation (date, puissance) VALUES (%s, %s)"),
		[row['Date'], row['Consommation']]  # TODO - check column names here
	)

# Commit and close the connection
conn.commit()
cur.close()
conn.close()

print("Données insérées avec succès!")
