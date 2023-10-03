"""
This script orchestrates the entire process from extracting audio from videos to 
transcribing the audio content.

It expects two mandatory command-line arguments: the path to the video and the desired name 
for the extracted audio file. An optional argument for the path to the Vosk model can also 
be provided.

Functions from the `extract_audio` module are utilized for audio extraction, and the 
`transcribe_audio_vosk` module is used for audio transcription.

Usage:
    python run.py <video_path> <audio_name> [--model_path <path_to_vosk_model>]

Example:
    python run.py sample_video.mp4 output_audio --model_path models/vosk/vosk-model-small-en-us-0.15

Note:
    This script was created as part of a larger project structure and might be expanded 
    to incorporate more functionalities or work with other modules in the future.
"""
import os
import argparse

from src.settings import settings
from src.modules.extract_audio import main as extract_audio_main
from src.modules.transcribe_audio_vosk import main as transcribe_audio_main


def main():
    """
    Parse the command-line arguments and orchestrate the video processing workflow.

    Expected arguments:
    - video_path: The path to the input video file.
    - audio_name: The desired name for the extracted audio output.
    - model_path (optional): The path to the Vosk model for audio transcription. 
      If not provided, the default model path in the `transcribe_audio_vosk` module will be used.

    This function sets up the argument parser and then:    
    1. Delegates the audio extraction to the `extract_audio_main` function.
    2. Delegates the audio transcription to the `transcribe_audio_main` function.
    """
    parser = argparse.ArgumentParser(description="Process video to transcribe audio.")
    parser.add_argument("video_path", help="Path to the video file.")
    parser.add_argument("audio_name", help="Name for the extracted audio file.")
    parser.add_argument("--model_path", help="Path to the Vosk model.")
    args = parser.parse_args()

    # Extracting audio
    audio_path = extract_audio_main(args.video_path, args.audio_name, settings.PATH_PROCESSED_AUDIO)

    json_name = os.path.splitext(args.audio_name)[0] + ".json"
    json_output_path = os.path.join(settings.PATH_PROCESSED_JSON, json_name)

    transcribe_audio_main(audio_path, args.model_path, json_output_path)

if __name__ == "__main__":
    main()
