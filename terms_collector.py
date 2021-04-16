import asyncio
import json
import os
import joblib
import time
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from entity.Dictionary import Dictionary
from repository.DictionaryRepository import DictionaryRepository
from repository.DocumentRepository import DocumentRepository

load_dotenv()


async def extract_terms():
    doc_repo = DocumentRepository()
    dictionary_repo = DictionaryRepository()
    while True:
        document = doc_repo.find_latest_unindexed()

        while document is not False:
            document.set_index_locked(True)
            doc_repo.update(document)

            html_content = document.get_content()
            if html_content is not None:
                print("Extracting data from ", document.get_url())
                dictionary_repo.delete_by_document(document)

                # Extract and process title terms
                title = extract_title(html_content)
                if title is not None:
                    words_frq = preprocess_text(title)
                    document.set_title(title)
                    store_text_words(words_frq, document, dictionary_repo)

                # Extract document description
                description = extract_description(html_content)
                if description is not None:
                    words_frq = preprocess_text(description)
                    document.set_description(description)
                    store_text_words(words_frq, document, dictionary_repo)
                    assumed_topic = assume_document_topic(description)
                    document.set_topic(assumed_topic)

                # Extract document contributors
                contributors = extract_contributors(html_content)
                if contributors is not None:
                    document.set_authors(json.dumps(contributors))
                    store_contributors(contributors, document, dictionary_repo)

                document.set_index_locked(False)
                document.set_indexed(True)
                doc_repo.update(document)
                print("Done!")
                print()
            document = doc_repo.find_latest_unindexed()

        print("Job complete, waiting", os.getenv('DOCUMENT_INDEXER_POLL'), "seconds for next run...")
        time.sleep(int(os.getenv('DOCUMENT_INDEXER_POLL')))


def assume_document_topic(description):
    multi_nb_model = joblib.load('topic_classifier/out/multi_nb_model.pkl')
    count_transformer = joblib.load('topic_classifier/out/model_count_transformer.pkl')
    tfidf_transformer = joblib.load('topic_classifier/out/model_tfidf_transformer.pkl')

    description_counts = count_transformer.transform([description])
    description_tfidf = tfidf_transformer.transform(description_counts)

    # Predict document topic using pre trained Multinomial Naïve Bayes ML model
    predicted_topic = multi_nb_model.predict(description_tfidf.toarray())
    return str(predicted_topic[0])


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
    if len(contributors) < 1:
        contributors = parser.findAll("meta", {"name": "DC.contributor"})
    if len(contributors) < 1:
        contributors = parser.findAll("meta", {"name": "dc.contributor"})
    if len(contributors) < 1:
        contributors = parser.findAll("meta", {"name": "dc.Contributor"})
    if len(contributors) < 1:
        contributors = parser.findAll("meta", {"name": "DC.Contributor.PersonalName"})
    if len(contributors) < 1:
        contributors = parser.findAll("meta", {"property": "article:author"})
    if len(contributors) < 1:
        contributors = parser.findAll("meta", {"property": "og:contributor"})
    if len(contributors) < 1:
        contributors = parser.findAll("meta", {"name": "dc.Creator"})
    if len(contributors) < 1:
        contributors = parser.findAll("meta", {"name": "dc.creator"})

    contributor_names = []
    for contributor in contributors:
        contributor_names.append(contributor["content"])
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


def store_text_words(words_frq, document, dictionary_repo):
    for word, frq in words_frq.items():
        dictionary = Dictionary()
        dictionary.set_document_id(document.get_id())
        dictionary.set_term(word)
        dictionary.set_term_frequency(frq)

        try:
            if dictionary_repo.find_by_term_and_doc(dictionary.get_term(), document) is False:
                dictionary_repo.add(dictionary)
        except:
            print("Problem Occurred Storing Word in Dictionary", dictionary.get_term())


def store_contributors(contributors, document, dictionary_repo):
    contributors_frq = {contributor: 1 for contributor in contributors}
    store_text_words(contributors_frq, document, dictionary_repo)


asyncio.get_event_loop().run_until_complete(extract_terms())

