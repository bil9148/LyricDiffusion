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
        if self.conn.closed != 0:
            self.connect()
