import os
import json
import time

from vosk import Model, KaldiRecognizer


def transcribe_audio_vosk(audio_path: str, model_path: str):
    model = Model(model_path)
    with open(audio_path, 'rb') as file:
        recognizer = KaldiRecognizer(model, 16000)
        data = file.read()
        recognizer.AcceptWaveform(data)
        result = recognizer.FinalResult()

    return json.loads(result)['text']


def save_to_json(data, path):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def format_time(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:  # 60 minutos * 60 segundos
        return f"{seconds / 60:.2f} minutes"
    else:
        return f"{seconds / 3600:.2f} hours"
    

if __name__ == '__main__':
    AUDIO_PATH = "data/processed/ptbr_short_example.wav"
    MODEL_PATH = "models/vosk/vosk-model-small-pt-0.3"

    file_name = os.path.basename(AUDIO_PATH)
    json_name = os.path.splitext(file_name)[0] + ".json"
    JSON_OUTPUT_PATH = os.path.join("data/processed", json_name)

    start_time = time.time()

    transcription = transcribe_audio_vosk(AUDIO_PATH, MODEL_PATH)

    elapsed_time = time.time() - start_time
    formatted_time = format_time(elapsed_time)

    data_to_save = {
        "name": file_name,
        "path": AUDIO_PATH,
        "processing_time": formatted_time,
        "transcription": transcription
    }

    save_to_json(data_to_save, JSON_OUTPUT_PATH)
    print(f"Transcript saved in: {JSON_OUTPUT_PATH}")
    print(f"Processing Time: {formatted_time}")
