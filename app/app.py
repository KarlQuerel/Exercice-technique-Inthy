#---	Imports		---#
from datetime import datetime
from flask import Flask, jsonify, request # Flask is a micro web framework for Python
import psycopg2 # PostgreSQL adapter for Python
import os # This module provides a way of using operating system dependent functionality
from	flask_cors import CORS # Flask extension for CORS (bonus)

#---	Debug Flag		---#
DEBUG = True

# Initializes the Flask app
app = Flask(__name__)

# Enables Cross-Origin Resource Sharing for the API (bonus)
CORS(app)

# Retrieves consumption data from a PostgreSQL database based on the date and time range.
def get_consumption_data(start_datetime, end_datetime):
	try:
		database_url = os.getenv('DATABASE_URL')

		if not database_url:
			raise ValueError("DATABASE_URL environment variable is not set.")

		if DEBUG == True:
			print(f"Connecting to database with URL: {database_url}")

		# Connects to PostgreSQL using psycopg2
		conn = psycopg2.connect(database_url)
		cur = conn.cursor()

		# Query to filter by both date & time
		query = """
			SELECT date, heures, puissance
			FROM consommation
			WHERE (date + heures) BETWEEN %s AND %s;
		"""

		if DEBUG == True:
			print(f"Executing Query: {query} with values ({start_datetime}, {end_datetime})")

		cur.execute(query, (start_datetime, end_datetime))
		data = cur.fetchall()

		cur.close()
		conn.close()

		return data

	except Exception as e:
		print(f"Error connecting to the database: {e}")
		return []

# Home route
@app.route('/')
def home():
	return "Bienvenue sur l'API de consommation énergétique !"

# API route to get consumption data
@app.route('/consommation', methods=['GET'])
def get_consumption():
	try:
		# Retrieve query parameters, with default values if not provided
		start_date = request.args.get('start_date', '2022-01-01 06:00:00')
		end_date = request.args.get('end_date', '2022-01-03 17:00:00')

		# Debugging
		if DEBUG == True:
			print(f"Received start_date: {start_date}, end_date: {end_date}")

		# Validate inputs
		if not start_date or not end_date:
			return jsonify({'error': 'start_date and end_date are required'}), 400

		# Convert input strings to datetime
		try:
			start_datetime = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
			end_datetime = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
		except ValueError:
			return jsonify({'error': 'Invalid date format. Expected: YYYY-MM-DD HH:MM:SS'}), 400

		# Fetch data from database
		data = get_consumption_data(start_datetime, end_datetime)

		if not data:
			return jsonify({'error': 'No data found for the given date range'}), 404

		# Calculate the average consumption and round it to 2 decimal places
		total_consumption = sum(row[2] for row in data)
		average_consumption = round(total_consumption / len(data), 2) if data else 0

		# Return response as JSON
		return jsonify({
			'average_consumption': average_consumption,
			'data': [
				{'datetime': f"{row[0]} {row[1]}", 'consommation': str(row[2])}
				for row in data
			]
		})

	except Exception as e:
		return jsonify({'error': str(e)}), 400

# host='0.0.0.0' makes the server publicly available
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')