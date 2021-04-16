from datetime import date, timedelta
from repository.Repository import Repository
from entity.Document import Document
from utils.Connection import Connection


class DocumentRepository(Repository):
    def __init__(self):
        connection = Connection()
        self.db, self.cursor = connection.get()

    def add(self, entity):
        if self.db is False:
            return False

        self.cursor.execute(
            "INSERT INTO documents (url, content, indexed, last_crawl, locked, screenshot, title, description, authors) VALUES (%(url)s, %(content)s, %(indexed)s, %(last_crawl)s, %(locked)s, %(screenshot)s, %(title)s, %(description)s, %(authors)s)",
            {
                'url': entity.get_url(),
                'content': entity.get_content(),
                'indexed': entity.is_indexed(),
                'last_crawl': entity.get_last_crawl(),
                'locked': entity.is_locked(),
                'screenshot': entity.get_screenshot(),
                'title': entity.get_title(),
                'description': entity.get_description(),
                'authors': entity.get_authors()
            }
        )
        self.db.commit()

        count = self.cursor.rowcount
        return count

    def update(self, entity):
        if self.db is False:
            return False

        self.cursor.execute(
            "UPDATE documents SET url=%(url)s, content=%(content)s, indexed=%(indexed)s, last_crawl=%(last_crawl)s, locked=%(locked)s, screenshot=%(screenshot)s, title=%(title)s, description=%(description)s, authors=%(authors)s WHERE id=%(id)s",
            {
                'url': entity.get_url(),
                'content': entity.get_content(),
                'indexed': entity.is_indexed(),
                'last_crawl': entity.get_last_crawl(),
                'locked': entity.is_locked(),
                'screenshot': entity.get_screenshot(),
                'id': entity.get_id(),
                'title': entity.get_title(),
                'description': entity.get_description(),
                'authors': entity.get_authors()
            }
        )
        self.db.commit()

        count = self.cursor.rowcount
        return count

    def find_by_url(self, url):
        if self.db is False:
            return False

        self.cursor.execute(
            "SELECT * FROM documents WHERE url = %(url)s LIMIT 1",
            {'url': url}
        )
        result = self.cursor.fetchone()

        if result is not None:
            return self.build_object(result)

        return False

    def find_latest_uncrawled(self):
        if self.db is False:
            return False

        last_week = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        self.cursor.execute(
            "SELECT * FROM documents WHERE (last_crawl IS NULL OR last_crawl < %(last_crawl)s) AND locked = 0 LIMIT 1",
            {'last_crawl': last_week}
        )
        result = self.cursor.fetchone()

        if result is not None:
            return self.build_object(result)

        return False

    def find_latest_unindexed(self):
        if self.db is False:
            return False

        self.cursor.execute(
            "SELECT * FROM documents WHERE content IS NOT NULL AND indexed = 0 LIMIT 1"
        )
        result = self.cursor.fetchone()

        if result is not None:
            return self.build_object(result)

        return False

    def build_object(self, result):
        document = Document()

        document.set_id(result['id'] if 'id' in result else None)
        document.set_url(result['url'] if 'url' in result else None)
        document.set_locked(result['locked'] if 'locked' in result else None)
        document.set_content(result['content'] if 'content' in result else None)
        document.set_indexed(result['indexed'] if 'indexed' in result else None)
        document.set_last_crawl(result['last_crawl'] if 'last_crawl' in result else None)
        document.set_description(result['description'] if 'description' in result else None)
        document.set_screenshot(result['screenshot'] if 'screenshot' in result else None)
        document.set_title(result['title'] if 'title' in result else None)
        document.set_authors(result['authors'] if 'authors' in result else None)

        return document
