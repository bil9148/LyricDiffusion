import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from gui import BasicUI

class Database:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )

            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        except psycopg2.Error as e:            
            BasicUI.HandleError(e)

    def disconnect(self):
        try:                
            if self.conn:
                self.conn.close()
                self.conn = None
        except psycopg2.Error as e:
            BasicUI.HandleError(e)

    def execute(self, query, params=None):
        try:
            self.check_connection()
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)

            return cursor
        except psycopg2.Error as e:
            BasicUI.HandleError(e)


    def fetch(self, query, params=None):
        try:
            self.check_connection()
            cursor = self.conn.cursor()
            cursor.execute(query, params)

            return cursor.fetchall()
            
        except psycopg2.Error as e:
            BasicUI.HandleError(e)


    def fetch_one(self, query, params=None):
        try:
            self.check_connection()
            cursor = self.conn.cursor()
            cursor.execute(query, params)

            return cursor.fetchone()
        
        except psycopg2.Error as e:
            BasicUI.HandleError(e)


    def check_connection(self):
        # If connection is not open, open it
        if self.conn is None or self.conn.closed != 0:
            self.connect()

    def setupAppDatabase(self):
        try:
            self.database = "postgres"

            # Check if lyrics2images database exists
            result = self.fetch_one("SELECT 1 FROM pg_database WHERE datname = %s", ("lyrics2images",))

            if result is None: 
                # Create lyrics2images database
                self.execute("CREATE DATABASE lyrics2images")

            # Create tables
            self.database = "lyrics2images"

            self.execute("CREATE TABLE IF NOT EXISTS configuration (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL UNIQUE)")
            
        except psycopg2.Error as e:
            BasicUI.HandleError(e)

database = Database("localhost", 5432, "postgres", "sqlpostgres", "postgres")