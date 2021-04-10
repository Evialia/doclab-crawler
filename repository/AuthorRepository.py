from datetime import date, timedelta

from entity.Author import Author
from repository.Repository import Repository
from entity.Document import Document
from utils.Connection import Connection


class AuthorRepository(Repository):
    def __init__(self):
        connection = Connection()
        self.db, self.cursor = connection.get()

    def add(self, entity):
        if self.db is False:
            return False

        self.cursor.execute(
            "INSERT INTO authors (url, last_crawl, locked) VALUES (%(url)s, %(last_crawl)s, %(locked)s)",
            {
                'url': entity.get_url(),
                'last_crawl': entity.get_last_crawl(),
                'locked': entity.is_locked()
            }
        )
        self.db.commit()

        count = self.cursor.rowcount
        return count

    def update(self, entity):
        if self.db is False:
            return False

        self.cursor.execute(
            "UPDATE authors SET url=%(url)s, last_crawl=%(last_crawl)s, locked=%(locked)s WHERE id=%(id)s",
            {
                'url': entity.get_url(),
                'last_crawl': entity.get_last_crawl(),
                'locked': entity.is_locked(),
                'id': entity.get_id()
            }
        )
        self.db.commit()

        count = self.cursor.rowcount
        return count

    def find_by_url(self, url):
        if self.db is False:
            return False

        self.cursor.execute(
            "SELECT * FROM authors WHERE url = %(url)s LIMIT 1",
            {'url': url}
        )
        result = self.cursor.fetchone()

        if result is not None:
            return self.build_object(result)

        return False

    def find_latest(self):
        if self.db is False:
            return False

        last_week = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        self.cursor.execute(
            "SELECT * FROM authors WHERE (last_crawl IS NULL OR last_crawl < %(last_crawl)s) AND locked = 0 LIMIT 1",
            {'last_crawl': last_week}
        )
        result = self.cursor.fetchone()

        if result is not None:
            return self.build_object(result)

        return False

    def build_object(self, result):
        author = Author()

        author.set_id(result['id'] if 'id' in result else None)
        author.set_url(result['url'] if 'url' in result else None)
        author.set_locked(result['locked'] if 'locked' in result else None)
        author.set_last_crawl(result['last_crawl'] if 'last_crawl' in result else None)

        return author
