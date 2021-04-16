class Document:
    def __init__(self):
        self.id = None
        self.url = None
        self.content = None
        self.indexed = None
        self.last_crawl = None
        self.locked = None
        self.index_locked = None
        self.title = None
        self.description = None
        self.authors = None
        self.topic = None
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

    def is_index_locked(self):
        return self.index_locked

    def set_index_locked(self, index_locked):
        self.index_locked = index_locked
        return self

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title
        return self

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description
        return self

    def get_authors(self):
        return self.authors

    def set_authors(self, authors):
        self.authors = authors
        return self

    def get_topic(self):
        return self.topic

    def set_topic(self, topic):
        self.topic = topic
        return self

    def get_screenshot(self):
        return self.screenshot

    def set_screenshot(self, screenshot):
        self.screenshot = screenshot
        return self
