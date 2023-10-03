import re


def segment_into_sentences(text):
    """
    Segment the provided text into sentences.

    Parameters:
    - text: The input text to be segmented into sentences.

    Returns:
    - A list of sentences.
    """
    return re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
