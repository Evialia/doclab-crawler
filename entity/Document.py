class Document:
    def __init__(self):
        self.id = None
        self.url = None
        self.content = None
        self.indexed = None
        self.last_crawl = None
        self.locked = None
        self.description = None
        self.screenshot = None

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

    def get_content(self):
        return self.content

    def set_content(self, content):
        self.content = content
        return self

    def is_indexed(self):
        return self.indexed

    def set_indexed(self, indexed):
        self.indexed = indexed
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

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description
        return self

    def get_screenshot(self):
        return self.description

    def set_screenshot(self, screenshot):
        self.screenshot = screenshot
        return self
