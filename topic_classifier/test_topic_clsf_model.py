from commons import testing_docs_csv, multi_nb_model_filename, model_count_transformer_filename, \
    model_tfidf_transformer_filename
import pandas
import numpy
import joblib


def test_topic_classifier_model():
    print("Loading trained model:", multi_nb_model_filename)
    multi_nb_model = joblib.load(multi_nb_model_filename)

    test_documents_df = extract_test_documents()
    test_documents_text = test_documents_df['text'].tolist()
    test_documents_topics = test_documents_df['topic'].tolist()

    predicted = predict_results(test_documents_text, multi_nb_model)
    accuracy = numpy.mean(predicted == test_documents_topics)
    print("Model's Accuracy:", accuracy)


def predict_results(test_documents_text, multi_nb_model):
    print("Loading Model's Count Transformer:", model_count_transformer_filename)
    count_transformer = joblib.load(model_count_transformer_filename)
    print("Loading Model's TF-IDF Transformer:", model_tfidf_transformer_filename)
    tfidf_transformer = joblib.load(model_tfidf_transformer_filename)

    print('Testing the Naïve Bayes Model...')
    test_documents_text_counts = count_transformer.transform(test_documents_text)
    test_documents_text_tfidf = tfidf_transformer.transform(test_documents_text_counts)
    predicted = multi_nb_model.predict(test_documents_text_tfidf.toarray())

    return predicted


def extract_test_documents():
    print('Extracting testing documents...')
    test_documents_df = pandas.read_csv(testing_docs_csv, index_col=0)
    return test_documents_df


if __name__ == '__main__':
    test_topic_classifier_model()
