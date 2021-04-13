from entity.Dictionary import Dictionary
from repository.Repository import Repository
from utils.Connection import Connection


class DictionaryRepository(Repository):
    def __init__(self):
        connection = Connection()
        self.db, self.cursor = connection.get()

    def add(self, entity):
        if self.db is False:
            return False

        self.cursor.execute(
            "INSERT INTO dictionary (document_id, term, term_frequency) VALUES (%(document_id)s, %(term)s, %(term_frequency)s)",
            {
                'document_id': entity.get_document_id(),
                'term': entity.get_term(),
                'term_frequency': entity.get_term_frequency()
            }
        )
        self.db.commit()

        count = self.cursor.rowcount
        return count

    def update(self, entity):
        if self.db is False:
            return False

        self.cursor.execute(
            "UPDATE dictionary SET document_id=%(document_id)s, term=%(term)s, term_frequency=%(term_frequency)s WHERE id=%(id)s",
            {
                'document_id': entity.get_document_id(),
                'term': entity.get_term(),
                'term_frequency': entity.get_term_frequency(),
                'id': entity.get_id()
            }
        )
        self.db.commit()

        count = self.cursor.rowcount
        return count

    def find_by_term_and_doc(self, term, document):
        if self.db is False:
            return False

        self.cursor.execute(
            "SELECT * FROM dictionary WHERE term = %(term)s AND document_id = %(doc_id)s LIMIT 1",
            {
                'term': term,
                'doc_id': document.get_id()
            }
        )
        result = self.cursor.fetchone()

        if result is not None:
            return self.build_object(result)

        return False

    def delete_by_document(self, document):
        if self.db is False:
            return False

        self.cursor.execute(
            "DELETE FROM dictionary WHERE document_id = %(doc_id)s",
            {
                'doc_id': document.get_id()
            }
        )
        self.db.commit()

        count = self.cursor.rowcount
        return count

    def build_object(self, result):
        dictionary = Dictionary()

        dictionary.set_id(result['id'] if 'id' in result else None)
        dictionary.set_document_id(result['document_id'] if 'document_id' in result else None)
        dictionary.set_term(result['term'] if 'term' in result else None)
        dictionary.set_term_frequency(result['term_frequency'] if 'term_frequency' in result else None)

        return dictionary
