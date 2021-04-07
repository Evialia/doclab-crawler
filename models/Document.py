from datetime import date, timedelta

import pyppeteer
from pyppeteer.errors import PageError


class Document:
    def __init__(self, url, connection):
        self.url = url
        self.db, self.cursor = connection.get()

    async def crawl_contents(self):
        browser = await pyppeteer.launch(args=['--no-sandbox'])
        browser_page = await browser.newPage()
        await browser_page.goto(self.url)

        try:
            print("CRAWLING: ", self.url)
            self.store_content(await browser_page.content())
        except PageError:
            print("Problem Occurred Crawling ", self.url)

        await browser_page.close()

    def store_content(self, content):
        current_time = date.today().strftime('%Y-%m-%d')

        if self.db is False:
            return False

        self.cursor.execute(
            "UPDATE documents SET content=%(content)s, last_crawl=%(last_crawl)s WHERE url=%(url)s",
            {'content': content, 'last_crawl': current_time, 'url': self.url}
        )
        self.db.commit()

        count = self.cursor.rowcount
        return count

    def store_url(self):
        if self.db is False:
            return False

        self.cursor.execute(
            "INSERT INTO documents (url) VALUES (%(url)s)",
            {'url': self.url}
        )
        self.db.commit()

        count = self.cursor.rowcount
        return count

    def does_url_exist(self):
        if self.db is False:
            return False

        self.cursor.execute(
            "SELECT * FROM documents WHERE url = %(url)s",
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
            "SELECT 1 FROM documents WHERE url = %s AND last_crawl > %s",
            (self.url, last_week)
        )

        self.cursor.fetchall()
        count = self.cursor.rowcount

        return count == 0

    def lock(self):
        if self.db is False:
            return False

        self.cursor.execute(
            "UPDATE documents SET locked = 1 WHERE url=%(url)s",
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
            "UPDATE documents SET locked = 0 WHERE url=%(url)s",
            {'url': self.url}
        )
        self.db.commit()
