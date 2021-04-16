from commons import document_topics, training_docs_csv, testing_docs_csv, csv_store_columns
from numpy.random import RandomState
import numpy
import os
import glob
import pandas


def process_documents():
    document_count = 0
    documents_df = pandas.DataFrame(columns=csv_store_columns)
    for topic in document_topics:
        topic_documents = extract_documents_by_topic(topic)

        for document in topic_documents:
            documents_df = documents_df.append({'doc_id': document_count, 'text': document, 'topic': topic}, ignore_index=True)
            document_count += 1

    store_as_training_testing_datasets(documents_df)


def extract_documents_by_topic(topic):
    print('Extracting documents by topic:', topic.upper())
    os.chdir(r'raw_training_data/' + topic)
    filenames = [file for file in glob.glob('*.txt')]

    documents_contents = []
    for name in filenames:
        file = open(name, 'r')
        try:
            file_content = file.read()
            documents_contents.append(file_content)
        except:
            print("Problem Occurred Reading File:", name)

    os.chdir(r'../../')
    return documents_contents


def store_as_training_testing_datasets(document_dataset_df):
    document_dataset_df = document_dataset_df.replace('', numpy.nan)
    document_dataset_df = document_dataset_df.dropna(axis='index', how='any')
    rand_state = RandomState()

    training_docs = document_dataset_df.sample(frac=0.8, random_state=rand_state)
    test_docs = document_dataset_df.loc[~document_dataset_df.index.isin(training_docs.index)]
    
    print('Storing training document set to:', training_docs_csv, ', count:', len(training_docs))
    training_docs.to_csv(training_docs_csv)
    
    print('Storing testing document set to:', testing_docs_csv, ', count:', len(test_docs))
    test_docs.to_csv(testing_docs_csv)


if __name__ == '__main__':
    process_documents()