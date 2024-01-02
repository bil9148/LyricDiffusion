import unittest
from db import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.testing_DB_name = "testing_db42069"
        self.database = Database(
            host="127.0.0.1", port="5432", user="postgres", password="sqlpostgres", database="postgres")

        self.database.connect()

        # Check if testing_db exists
        result = self.database.fetch_one(
            f"SELECT 1 FROM pg_database WHERE datname = '{self.testing_DB_name}'")

        if not result:
            # Drop testing_db if it exists
            self.database.execute(
                f"DROP DATABASE IF EXISTS {self.testing_DB_name}")
            # Create testing_db
            self.database.execute(f"CREATE DATABASE {self.testing_DB_name}")

        # Connect to testing_db
        self.database.database = self.testing_DB_name

    def tearDown(self):
        # Drop testing_db
        self.database.database = "postgres"

        self.database.execute(f"DROP DATABASE IF EXISTS {self.testing_DB_name}")

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

    def test_setupDatabase(self):
        # Check if lyrics2images database exists
        self.database.setupDatabase()

        result = self.database.fetch_one("SELECT 1 FROM pg_database WHERE datname = 'lyrics2images'")

        self.assertIsNotNone(result, "lyrics2images database should exist")


if __name__ == "__main__":
    unittest.main()
