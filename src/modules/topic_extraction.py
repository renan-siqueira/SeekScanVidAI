"""
Module for topic extraction from transcribed audio content.

This module provides functionalities to process a given transcription 
(in the form of text) to extract main topics using Latent Dirichlet Allocation (LDA). 
The input for the topic extraction process is provided via a JSON file 
that contains the transcription. The results (extracted topics) are then saved 
back to the same JSON file.

Dependencies:
- gensim: Used for LDA model creation and topic extraction.
- utils: Contains utility functions for text segmentation.
"""
import json
import string

from gensim import corpora, models

from .utils import segment_into_sentences


def preprocess_text(text, stopwords):
    """Tokenize, remove punctuation and remove stopwords."""
    translator = str.maketrans('', '', string.punctuation)
    return [word for word in text.translate(translator).lower().split() if word not in stopwords]


def extract_topics_from_transcription(transcription, stopwords, num_topics=2):
    """Extract main topics from given transcription using LDA."""
    texts = [
        preprocess_text(sentence, stopwords) for sentence in segment_into_sentences(transcription)
    ]

    # Create a dictionary and a corpus for LDA
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # Create the LDA model
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

    topics = lda_model.print_topics(num_words=5)
    return [topic[1] for topic in topics]


def main(json_input_path, stopwords):
    """
    Extract main topics from a transcription stored in a JSON file and update the file with 
    the results.

    The function reads the transcription from a given JSON file, extracts topics 
    using the LDA algorithm, and then saves the extracted topics back to the same JSON file.

    Parameters:
    - json_input_path (str): Path to the JSON file containing the transcription.
    - stopwords (set): A set of words to be excluded during topic extraction.

    """
    with open(json_input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    transcription = data['transcription']

    data["topics"] = extract_topics_from_transcription(transcription, stopwords)

    with open(json_input_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
