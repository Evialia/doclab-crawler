import pyppeteer
from pyppeteer.errors import PageError
from db_utils import get_connection, close_connection, store_content


class Document:
    def __init__(self, url):
        self.url = url

    async def crawl_contents(self):
        browser = await pyppeteer.launch()
        browser_page = await browser.newPage()
        await browser_page.goto(self.url)

        try:
            print("CRAWLING: ", self.url)
            store_content(self.url, await browser_page.content())
        except PageError:
            print("Problem Occurred Crawling ", self.url)

        await browser_page.close()

    def lock(self):
        db, cursor = get_connection()
        cursor.execute(
            "UPDATE pages SET locked = 1 WHERE url=%(url)s",
            {'url': self.url}
        )
        db.commit()
        count = cursor.rowcount
        close_connection(db, cursor)

        if count == 1:
            return True
        return False

    def unlock(self):
        db, cursor = get_connection()
        cursor.execute(
            "UPDATE pages SET locked = 0 WHERE url=%(url)s",
            {'url': self.url}
        )
        db.commit()
        close_connection(db, cursor)
