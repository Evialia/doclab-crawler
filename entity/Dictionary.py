class Dictionary:
    def __init__(self):
        self.id = None
        self.document_id = None
        self.term = None
        self.term_frequency = None

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id
        return self

    def get_document_id(self):
        return self.document_id

    def set_document_id(self, document_id):
        self.document_id = document_id
        return self

    def get_term(self):
        return self.term

    def set_term(self, term):
        self.term = term
        return self

    def get_term_frequency(self):
        return self.term_frequency

    def set_term_frequency(self, term_frequency):
        self.term_frequency = term_frequency
        return self
