"""
Module to transcribe audio using Vosk and some utility functions.
"""
import os
import json
import time

from vosk import Model, KaldiRecognizer
from pydub import AudioSegment


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


def transcribe_by_chunks(audio_path: str, model_path: str, chunk_length: int = 60000) -> str:
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
    chunk_dir = f'data/processed/audio/chunk/{audio_name}/'
    if not os.path.exists(chunk_dir):
        os.makedirs(chunk_dir)

    audio = AudioSegment.from_wav(audio_path)
    num_chunks = len(audio) // chunk_length + (1 if len(audio) % chunk_length else 0)

    transcriptions = []
    for i in range(num_chunks):
        start_time = i * chunk_length
        end_time = (i+1) * chunk_length
        chunk = audio[start_time:end_time]

        chunk_filename = os.path.join(chunk_dir, f'chunk_{i}.wav')
        chunk.export(chunk_filename, format='wav')
        chunk_transcription = transcribe_audio_vosk(chunk_filename, model_path)
        transcriptions.append(chunk_transcription)

    return ' '.join(transcriptions)


if __name__ == '__main__':
    AUDIO_PATH = "data/processed/audio/ptbr_short_example.wav"
    MODEL_PATH = "models/vosk/vosk-model-small-pt-0.3"

    file_name = os.path.basename(AUDIO_PATH)
    json_name = os.path.splitext(file_name)[0] + ".json"
    JSON_OUTPUT_PATH = os.path.join("data/processed/json", json_name)

    START_TIME = time.time()

    TRANSCRIPTION = transcribe_by_chunks(AUDIO_PATH, MODEL_PATH)

    elapsed_time = time.time() - START_TIME
    formatted_time = format_time(elapsed_time)

    data_to_save = {
        "name": file_name,
        "path": AUDIO_PATH,
        "processing_time": formatted_time,
        "transcription": TRANSCRIPTION
    }

    save_to_json(data_to_save, JSON_OUTPUT_PATH)
    print(f"Transcript saved in: {JSON_OUTPUT_PATH}")
    print(f"Processing Time: {formatted_time}")
