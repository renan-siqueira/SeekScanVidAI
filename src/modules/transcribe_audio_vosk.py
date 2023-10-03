"""
Module to transcribe audio using Vosk and some utility functions.
"""
import os
import json
import time
import re
import string

import RAKE
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
from gensim import corpora, models


rake = RAKE.Rake(RAKE.SmartStopList())


def transcribe_audio_vosk(audio_path: str, model_path: str):
    """
    Transcribe an audio file using the Vosk library.

    Parameters:
    - audio_path: Path to the audio file.
    - model_path: Path to the Vosk model.

    Returns:
    - Transcription of the audio.
    """
    model = Model(model_path)
    with open(audio_path, 'rb') as file:
        recognizer = KaldiRecognizer(model, 16000)
        data = file.read()
        recognizer.AcceptWaveform(data)
        result = recognizer.FinalResult()

    return json.loads(result)['text']


def save_to_json(data, path):
    """
    Save a dictionary to a JSON file.

    Parameters:
    - data: Dictionary to save.
    - path: Path to the JSON file.
    """
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def format_time(seconds: float) -> str:
    """
    Format time in seconds to a string representation.

    Parameters:
    - seconds: Time in seconds.

    Returns:
    - Formatted string representation of the time.
    """
    if seconds < 60:
        return f"{seconds:.2f} seconds"

    if seconds < 3600:  # 60 minutos * 60 segundos
        return f"{seconds / 60:.2f} minutes"

    return f"{seconds / 3600:.2f} hours"


def transcribe_by_chunks(audio_path: str, model_path: str, chunk_length: int = 10000) -> tuple:
    """
    Transcribe an audio file by splitting it into chunks.

    Parameters:
    - audio_path: Path to the audio file.
    - model_path: Path to the Vosk model.
    - chunk_length: Length of each chunk in milliseconds.

    Returns:
    - Transcription of the audio.
    """
    audio_name = os.path.splitext(os.path.basename(audio_path))[0]
    chunk_dir = os.path.join('data', 'processed', 'audio', 'chunk', audio_name)

    os.makedirs(chunk_dir, exist_ok=True)

    audio = AudioSegment.from_wav(audio_path)
    num_chunks = len(audio) // chunk_length + bool(len(audio) % chunk_length)

    transcriptions = []
    indices = []
    for i in range(num_chunks):
        chunk = audio[i * chunk_length:(i+1) * chunk_length]
        chunk_filename = os.path.join(chunk_dir, f'chunk_{i}.wav')
        chunk.export(chunk_filename, format='wav')

        transcription = transcribe_audio_vosk(chunk_filename, model_path)
        transcriptions.append(transcription)

        chunk_indices = generate_index_for_chunk(transcription, i * chunk_length, chunk_length)
        indices.extend(chunk_indices)

    return ' '.join(transcriptions), indices


def extract_keywords(text):
    """
    Extract keywords from the given text.

    Parameters:
    - text: The input text from which keywords are to be extracted.

    Returns:
    - A list of keywords extracted from the text.
    """
    return rake.run(text)


def segment_into_sentences(text):
    """
    Segment the provided text into sentences.

    Parameters:
    - text: The input text to be segmented into sentences.

    Returns:
    - A list of sentences.
    """
    return re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)


def generate_index_for_chunk(transcription, start_time_ms, chunk_length):
    """
    Generate index data for a given audio chunk.

    Parameters:
    - transcription: The transcribed text of the audio chunk.
    - start_time_ms: The starting time of the chunk in milliseconds.
    - chunk_length: The length of the chunk in milliseconds.

    Returns:
    - A list of index data with keyword, score, and start time for each sentence 
    in the transcription.
    """
    sentences = segment_into_sentences(transcription)

    total_length = sum(len(sentence) for sentence in sentences)

    index = []
    time_elapsed = 0  # Time elapsed since the start of the chunk
    for _, sentence in enumerate(sentences):
        keywords = extract_keywords(sentence)

        # Calculate the proportion of this sentence to the total transcription of the chunk.
        sentence_proportion = len(sentence) / total_length if total_length else 0

        # Estimate how long this sentence takes within the chunk.
        sentence_duration_ms = chunk_length * sentence_proportion
        estimated_start_time_seconds = (start_time_ms + time_elapsed) / 1000  # Convert to seconds

        for keyword, score in keywords:
            entry = {
                'keyword': keyword,
                'score': score,
                'start_time': format_time(estimated_start_time_seconds)
            }
            index.append(entry)

        time_elapsed += sentence_duration_ms

    return index


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


def main(audio_path: str, model_path: str, json_output_path: str, stopwords: set):
    """Main function to handle the audio transcription process."""
    start_time = time.time()

    transcription, indices = transcribe_by_chunks(audio_path, model_path)
    topics = extract_topics_from_transcription(transcription, stopwords)

    elapsed_time = time.time() - start_time
    formatted_time = format_time(elapsed_time)

    data_to_save = {
        "name": os.path.basename(audio_path),
        "path": audio_path,
        "processing_time": formatted_time,
        "transcription": transcription,
        'topics': topics,
        'indices': indices
    }

    save_to_json(data_to_save, json_output_path)
    print(f"Transcript saved in: {json_output_path}")
    print(f"Processing Time: {formatted_time}")
