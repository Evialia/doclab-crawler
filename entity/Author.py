class Author:
    def __init__(self):
        self.id = None
        self.url = None
        self.last_crawl = None
        self.locked = None

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id
        return self

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url
        return self

    def get_last_crawl(self):
        return self.last_crawl

    def set_last_crawl(self, last_crawl):
        self.last_crawl = last_crawl
        return self

    def is_locked(self):
        return self.locked

    def set_locked(self, locked):
        self.locked = locked
        return self
