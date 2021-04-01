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

    count = cursor.rowcount
    close_connection(db, cursor)
    return count


def store_content(url, content):
    current_time = date.today().strftime('%Y-%m-%d')
    db, cursor = get_connection()

    cursor.execute(
        "UPDATE pages SET content=%(content)s, last_crawl=%(last_crawl)s WHERE url=%(url)s",
        {'content': content, 'last_crawl': current_time, 'url': url}
    )
    db.commit()

    count = cursor.rowcount
    close_connection(db, cursor)
    return count


def store_url(url):
    db, cursor = get_connection()

    cursor.execute(
        "INSERT INTO pages (url) VALUES (%(url)s)",
        {'url': url}
    )
    db.commit()

    count = cursor.rowcount
    close_connection(db, cursor)
    return count


def does_url_exist(url):
    db, cursor = get_connection()
    cursor.execute(
        "SELECT * FROM pages WHERE url = %(url)s",
        {'url': url}
    )

    cursor.fetchall()
    count = cursor.rowcount
    close_connection(db, cursor)

    return count == 1


def check_crawl_required(url):
    last_week = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    db, cursor = get_connection()

    # Only get results if URL is found and has been crawled within the past week
    cursor.execute(
        "SELECT 1 FROM pages WHERE url = %s AND last_crawl > %s",
        (url, last_week)
    )

    cursor.fetchall()
    count = cursor.rowcount
    close_connection(db, cursor)

    return count == 0


def get_next_url():
    last_week = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    db, cursor = get_connection()
    cursor.execute("SELECT url FROM pages WHERE (last_crawl IS NULL OR last_crawl < %(date)s) AND locked = 0 LIMIT 1", {'date': last_week})
    result = cursor.fetchone()

    close_connection(db, cursor)

    if result is not None:
        return result[0]
    else:
        return None


def close_connection(db, cursor):
    cursor.close()
    db.close()

