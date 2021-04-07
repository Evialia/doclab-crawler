from dotenv import load_dotenv
import mysql.connector
import os
import time

load_dotenv()

class Connection:
    def __init__(self):
        self.db = False
        self.cursor = False

    def get(self):
        if self.db is not False:
            self.db.ping(True)
            return self.db, self.cursor

        self.get_connection()

        return self.db, self.cursor


    def attempt_connection(self):
        try:
            print("Attempting to get connection")
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASS'),
                database=os.getenv('DB_NAME'),
            )
            self.db = connection
            self.cursor = self.db.cursor()

        except mysql.connector.Error as err:
            print("Could not get connection: {}".format(err))
            self.db = False
            self.cursor = False


    def get_connection(self):
        print("Attempting to connect DB...")

        self.attempt_connection()
        while not self.db:
            time.sleep(int(os.getenv('CHECK_DB_WAIT')))
            print("Could not establish DB connection")
            self.attempt_connection()

        print("DB connection established!")

        print("Checking for schema initialization...")

        db_exists = False
        while not db_exists:
            self.cursor.execute("SHOW DATABASES LIKE 'doclab'")
            result = self.cursor.fetchone()
            if result is not None:
                db_exists = True
            else:
                print("Schema not initialized")
            time.sleep(int(os.getenv('CHECK_DB_WAIT')))

        print("Schema initialized!")


    def close(self):
        self.cursor.close()
        self.db.close()


