"""
This script orchestrates the entire process from extracting audio from videos to 
transcribing the audio content.

It expects two mandatory command-line arguments: the path to the video and the desired name 
for the extracted audio file. An optional argument for the path to the Vosk model can also 
be provided.

Functions from the `extract_audio` module are utilized for audio extraction, and the 
`transcribe_audio_vosk` module is used for audio transcription.

Usage:
    python run.py <video_path> <audio_name> [--language <either 'en' or 'pt'>]

Example:
    python run.py sample_video.mp4 output_audio --language pt

Note:
    This script was created as part of a larger project structure and might be expanded 
    to incorporate more functionalities or work with other modules in the future.
"""
import os
import argparse

from langdetect import detect

from src.settings import settings
from src.modules.extract_audio import main as extract_audio_main
from src.modules.transcribe_audio_vosk import main as transcribe_audio_main


def detect_language(text):
    """Detect the language of the given text."""
    try:
        return detect(text)
    except:
        return 'unknown'


def main():
    """
    Parse the command-line arguments and orchestrate the video processing workflow.

    Expected arguments:
    - video_path: The path to the input video file.
    - audio_name: The desired name for the extracted audio output.
    - language: The language of the audio content (either 'en' or 'pt').

    This function sets up the argument parser and then:    
    1. Delegates the audio extraction to the `extract_audio_main` function.
    2. Delegates the audio transcription to the `transcribe_audio_main` function based 
    on the specified language.
    """
    parser = argparse.ArgumentParser(description="Process video to transcribe audio.")
    parser.add_argument("video_path", help="Path to the video file.")
    parser.add_argument("audio_name", help="Name for the extracted audio file.")
    parser.add_argument(
        "--language",
        choices=['en', 'pt'],
        required=True,
        help="Language of the audio content (either 'en' or 'pt')."
    )

    args = parser.parse_args()

    if args.language == 'en':
        model_path = settings.PATH_MODEL_EN
        stopwords = settings.STOPWORDS_EN
    elif args.language == 'pt':
        model_path = settings.PATH_MODEL_PT
        stopwords = settings.STOPWORDS_PT
    else:
        raise ValueError("Language not supported.")

    # Extracting the audio
    audio_path = extract_audio_main(
        args.video_path,
        args.audio_name,
        settings.PATH_PROCESSED_AUDIO,
    )

    json_name = os.path.splitext(args.audio_name)[0] + ".json"
    json_output_path = os.path.join(settings.PATH_PROCESSED_JSON, json_name)

    # Transcribing the audio using the appropriate model
    transcribe_audio_main(audio_path, model_path, json_output_path, stopwords)

if __name__ == "__main__":
    main()
