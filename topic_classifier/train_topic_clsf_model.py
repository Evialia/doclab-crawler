from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from commons import training_docs_csv, multi_nb_model_filename, model_count_transformer_filename, \
    model_tfidf_transformer_filename
import pandas
import joblib


def train_topic_classifier_model():
    count_transformer = CountVectorizer()
    tfidf_transformer = TfidfTransformer()

    train_documents_df = extract_train_documents()
    train_documents_text = train_documents_df['text'].tolist()
    train_documents_topics = train_documents_df['topic'].tolist()

    print('Training the Naïve Bayes Model...')
    trained_model = multi_nb_clf_train(count_transformer, tfidf_transformer, train_documents_text, train_documents_topics)

    print("Storing trained model to:", multi_nb_model_filename)
    joblib.dump(trained_model, multi_nb_model_filename)
    print("Storing Model's Count Transformer to:", model_count_transformer_filename)
    joblib.dump(count_transformer, model_count_transformer_filename)
    print("Storing Model's TF-IDF Transformer to:", model_tfidf_transformer_filename)
    joblib.dump(tfidf_transformer, model_tfidf_transformer_filename)


def multi_nb_clf_train(count_transformer, tfidf_transformer, input_data, output_topic):
    train_documents_text_counts = count_transformer.fit_transform(input_data)
    train_documents_text_tfidf = tfidf_transformer.fit_transform(train_documents_text_counts)
    multi_nb = MultinomialNB().fit(train_documents_text_tfidf, output_topic)
    return multi_nb


def extract_train_documents():
    print('Extracting training documents...')
    train_documents_df = pandas.read_csv(training_docs_csv, index_col=0)
    return train_documents_df


if __name__ == '__main__':
    train_topic_classifier_model()
