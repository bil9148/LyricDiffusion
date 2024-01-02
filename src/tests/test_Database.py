import unittest
from db import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database = Database(
            host="127.0.0.1", port="5432", user="postgres", password="sqlpostgres", database="postgres")

        self.database.connect()

        # Check if testing_db exists
        result = self.database.fetch_one("SELECT 1 FROM pg_database WHERE datname = %s", ("testing_db",))

        if not result:
            # Drop testing_db if it exists
            self.database.execute("DROP DATABASE IF EXISTS testing_db")
            # Create testing_db
            self.database.execute("CREATE DATABASE testing_db")

        # Connect to testing_db
        self.database.database = "testing_db"

    def tearDown(self):
        self.database.disconnect()

    def test_connection(self):
        self.assertIsNotNone(self.database.conn,
                             "Connection should be established")

    def test_execute(self):
        query = "SELECT 1"
        result = self.database.execute(query)
        self.assertIsNotNone(result, "Execute should return a cursor")

    def test_fetch(self):
        query = "SELECT 1"
        result = self.database.fetch(query)
        self.assertIsNotNone(result, "Fetch should return a result set")

    def test_fetch_one(self):
        query = "SELECT 1"
        result = self.database.fetch_one(query)
        self.assertIsNotNone(result, "Fetch_one should return a single result")

    def test_disconnect(self):
        self.database.disconnect()
        self.assertIsNone(self.database.conn, "Connection should be closed")


if __name__ == "__main__":
    unittest.main()
