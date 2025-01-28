#---	Imports		---#
import unittest
from app import app

class TestAPI(unittest.TestCase):

	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True

	def test_consumption(self):
		response = self.app.get('/consommation?start_date=2022-01-01%2006:00:00&end_date=2022-01-03%2017:00:00')
		self.assertEqual(response.status_code, 200)
		self.assertIn('average_consumption', response.json)

if __name__ == '__main__':
	unittest.main()
