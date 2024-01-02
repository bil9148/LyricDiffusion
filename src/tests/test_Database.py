import unittest
from db import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.testing_DB_name = "testing_db42069"
        self.database = Database(
            host="127.0.0.1", port="5432", user="postgres", password="sqlpostgres", database="postgres")

        self.database.setupTestingDatabase()

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
        self.database.setupDatabase("testing_db42069")

        result = self.database.fetch_one(
            "SELECT 1 FROM pg_database WHERE datname = 'testing_db42069'")

        self.assertIsNotNone(
            result, "testing_db42069 database should exist")

    def test_createTable(self):
        self.database.execute("drop table if exists test_table")

        self.database.execute("create table test_table (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL UNIQUE)")

        result = self.database.fetch_one("SELECT 1 FROM pg_tables WHERE tablename = 'test_table'")

        self.assertIsNotNone(result, "test_table should exist")

    def test_insert(self):
        self.database.execute("drop table if exists test_table")
        
        self.database.execute("create table test_table (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL UNIQUE)")

        self.database.execute("insert into test_table (name) values (%s)", ("test",))

        result = self.database.fetch_one("select * from test_table where name = %s", ("test",))

        self.assertIsNotNone(result, "test_table should contain the inserted row")

if __name__ == "__main__":
    unittest.main()
