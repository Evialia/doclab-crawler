import asyncio
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from entity.Dictionary import Dictionary
from repository.DictionaryRepository import DictionaryRepository
from repository.DocumentRepository import DocumentRepository


async def extract_terms():
    doc_repo = DocumentRepository()
    dictionary_repo = DictionaryRepository()
    document = doc_repo.find_latest_unindexed()

    while document is not False:
        html_content = document.get_content()
        dictionary_repo.delete_by_document(document)

        # Extract and process title terms
        title = extract_title(html_content)
        if title is not None:
            document.set_title(title)
            store_text_words(title, document, dictionary_repo)

        # Extract document description
        description = extract_description(html_content)
        if description is not None:
            document.set_description(description)
            store_text_words(description, document, dictionary_repo)

        contributors = extract_contributors(html_content)
        if contributors is not None:
            document.set_authors(contributors)
            store_text_words(contributors, document, dictionary_repo)

        # Do indexing here
        document.set_indexed(True)

        doc_repo.update(document)
        document = doc_repo.find_latest_unindexed()


def extract_description(html_content):
    parser = BeautifulSoup(html_content, "html.parser")

    description = parser.find("meta", {"name": "DC.Description"})
    if description is None:
        description = parser.find("meta", {"name": "dc.description"})
    if description is None:
        description = parser.find("meta", {"name": " DC.description"})
    if description is None:
        description = parser.find("meta", {"name": "dc.Description"})
    if description is None:
        description = parser.find("meta", {"property": "og:description"})
    if description is None:
        description = parser.find("meta", {"name": "og-description"})
    if description is None:
        description = parser.find("meta", {"name": "description"})

    if description is not None:
        clean_description = BeautifulSoup(description["content"], "html.parser").text
        return clean_description
    return None


def extract_title(html_content):
    parser = BeautifulSoup(html_content, "html.parser")

    title = parser.find("meta", {"name": "DC.Title"})
    if title is None:
        title = parser.find("meta", {"name": "dc.title"})
    if title is None:
        title = parser.find("meta", {"name": "DC.title"})
    if title is None:
        title = parser.find("meta", {"name": "dc.Title"})
    if title is None:
        title = parser.find("meta", {"property": "og:title"})
    if title is None:
        title = parser.find("meta", {"name": "og-title"})
    if title is None:
        title = parser.find("meta", {"name": "title"})

    if title is not None:
        clean_title = BeautifulSoup(title["content"], "html.parser").text
        return clean_title
    return None


def extract_contributors(html_content):
    parser = BeautifulSoup(html_content, "html.parser")

    contributors = parser.findAll("meta", {"name": "DC.Contributor"})
    if contributors is None:
        contributors = parser.findAll("meta", {"name": "DC.contributor"})
    if contributors is None:
        contributors = parser.findAll("meta", {"name": "dc.contributor"})
    if contributors is None:
        contributors = parser.findAll("meta", {"name": "dc.Contributor"})
    if contributors is None:
        contributors = parser.findAll("meta", {"property": "og:contributor"})
    if contributors is None:
        contributors = parser.findAll("meta", {"name": "dc.Creator"})
    if contributors is None:
        contributors = parser.findAll("meta", {"name": "dc.creator"})

    contributor_names = []
    for contributor in contributors:
        contributor_names.append(contributor["content"])

    print("CONTRIBUTORS >> ", contributor_names)
    return contributor_names


def preprocess_text(text):
    sw = stopwords.words('english')
    stemmer = PorterStemmer()

    text = text.lower()
    words = word_tokenize(text)

    processed_words = []
    for word in words:
        if word not in sw and len(word) >= 3:
            processed_words.append(stemmer.stem(word))

    word_frq = {word: processed_words.count(word) for word in processed_words}
    return word_frq


def store_text_words(text, document, dictionary_repo):
    words_frq = preprocess_text(text)

    for word, frq in words_frq.items():
        dictionary = Dictionary()
        dictionary.set_document_id(document.get_id())
        dictionary.set_term(word)
        dictionary.set_term_frequency(frq)

        if dictionary_repo.find_by_term_and_doc(dictionary.get_term(), document) is False:
            dictionary_repo.add(dictionary)


asyncio.get_event_loop().run_until_complete(extract_terms())

