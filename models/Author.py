from datetime import date, timedelta

class Author:
    def __init__(self, url, connection):
        self.url = url
        self.db, self.cursor = connection.get()

    def store_url(self):
        if self.db is False:
            return False

        self.cursor.execute(
            "INSERT INTO authors (url) VALUES (%(url)s)",
            {'url': self.url}
        )
        self.db.commit()

        count = self.cursor.rowcount
        return count

    def does_url_exist(self):
        if self.db is False:
            return False

        self.cursor.execute(
            "SELECT * FROM authors WHERE url = %(url)s",
            {'url': self.url}
        )

        self.cursor.fetchall()
        count = self.cursor.rowcount

        return count == 1

    def check_crawl_required(self):
        last_week = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')

        if self.db is False:
            return False

        # Only get results if URL is found and has been crawled within the past week
        self.cursor.execute(
            "SELECT 1 FROM authors WHERE url = %s AND last_crawl > %s",
            (self.url, last_week)
        )

        self.cursor.fetchall()
        count = self.cursor.rowcount

        return count == 0

    def lock(self):
        if self.db is False:
            return False

        self.cursor.execute(
            "UPDATE authors SET locked = 1 WHERE url=%(url)s",
            {'url': self.url}
        )
        self.db.commit()
        count = self.cursor.rowcount

        if count == 1:
            return True
        return False

    def unlock(self):
        if self.db is False:
            return False

        self.cursor.execute(
            "UPDATE authors SET locked = 0 WHERE url=%(url)s",
            {'url': self.url}
        )
        self.db.commit()
