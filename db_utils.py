import mysql.connector
from datetime import date
from datetime import timedelta

mysql.connector.connect(
    host="localhost",
    port="8889",
    user="root",
    password="root",
    database="doclab",
    pool_name="crawler_pool",
    pool_size=15
)


def get_connection():
    db = mysql.connector.connect(pool_name='crawler_pool')
    return db, db.cursor()


def store(url, content):
    current_time = date.today().strftime('%Y-%m-%d')
    db, cursor = get_connection()

    cursor.execute(
        "INSERT INTO pages (url, content, last_crawl) VALUES (%s, %s, %s)",
        (url, content, current_time)
    )
    db.commit()

    return cursor.rowcount


def check_crawl_required(url):
    last_week = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    db, cursor = get_connection()

    # Only get results if URL is found and has been crawled within the past week
    cursor.execute(
        "SELECT 1 FROM pages WHERE url = %s AND last_crawl > %s",
        (url, last_week)
    )
    cursor.fetchall()

    # Return true if NO result is found
    return cursor.rowcount == 0

