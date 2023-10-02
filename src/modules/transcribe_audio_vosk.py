import os
import json

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


if __name__ == '__main__':
    AUDIO_PATH = "data/processed/ptbr_example.wav"
    MODEL_PATH = "models/vosk/vosk-model-small-pt-0.3"

    file_name = os.path.basename(AUDIO_PATH)
    json_name = os.path.splitext(file_name)[0] + ".json"
    JSON_OUTPUT_PATH = os.path.join("data/processed", json_name)

    transcription = transcribe_audio_vosk(AUDIO_PATH, MODEL_PATH)

    data_to_save = {
        "name": file_name,
        "path": AUDIO_PATH,
        "transcription": transcription
    }

    save_to_json(data_to_save, JSON_OUTPUT_PATH)
    print(f"Transcript saved in: {JSON_OUTPUT_PATH}")
