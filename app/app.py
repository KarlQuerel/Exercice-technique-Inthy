#---	Imports		---#
from	datetime import datetime
from	flask import Flask, jsonify, request
import	psycopg2
import	os

#---	Debug Flags		---#
DEBUG = True

app = Flask(__name__)

# Fonction pour récupérer les données de la base
def get_consumption_data(start_date, end_date):
	try:
		# Retrieve the database connection URL from the environment variable
		database_url = os.environ.get('DATABASE_URL')

		if not database_url:
			raise ValueError("DATABASE_URL environment variable is not set.")

		if DEBUG == True:
			print(f"Connecting to database with URL: {database_url}")


		# Connect to the PostgreSQL database using the connection string
		conn = psycopg2.connect(database_url)

		cur = conn.cursor()

		query = """
			SELECT date, puissance
			FROM consommation
			WHERE date BETWEEN %s AND %s;
		"""

		# Executing query
		cur.execute(query, (start_date, end_date))
		data = cur.fetchall()

		cur.close()
		conn.close()

		return data

	except Exception as e:
		print(f"Error connecting to the database: {e}")
		return []

# Route for the root URL
@app.route('/')
def home():
	return "Bienvenue sur l'API de consommation énergétique !"

# API route to get consumption data
@app.route('/consommation', methods=['GET'])
def get_consumption():
	try:
		# Récupérer les paramètres de la requête (start_date et end_date)
		start_date = request.args.get('start_date')
		end_date = request.args.get('end_date')

		# Print for debugging
		print(f"Received start_date: {start_date}, end_date: {end_date}")

		# Check if the parameters are provided
		if not start_date or not end_date:
			return jsonify({'error': 'start_date and end_date are required'}), 400

		# Try to convert the date strings to datetime objects
		try:
			start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
			end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
		except ValueError:
			return jsonify({'error': 'Invalid date format. Expected format: YYYY-MM-DD HH:MM:SS'}), 400

		# Retrieve the data from the database
		data = get_consumption_data(start_date, end_date)

		if not data:
			return jsonify({'error': 'No data found for the given date range'}), 404

		# Calculate the average consumption
		total_consumption = sum([row[1] for row in data])
		average_consumption = total_consumption / len(data) if data else 0

		# Return the response in JSON format
		return jsonify({
			'average_consumption': average_consumption,
			'data': [{'date': row[0].strftime('%Y-%m-%d %H:%M:%S'), 'consommation': row[1]} for row in data]
		})
	
	except Exception as e:
		return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
