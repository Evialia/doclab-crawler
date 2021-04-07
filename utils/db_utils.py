import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    database=os.getenv('DB_NAME'),
    pool_name="crawler_pool",
    pool_size=int(os.getenv('CONNECTION_POOL_COUNT'))
)


def get_connection():
    db = mysql.connector.connect(pool_name='crawler_pool')
    return db, db.cursor()


def close_connection(db, cursor):
    cursor.close()
    db.close()

