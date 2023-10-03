# SeekScanVidAI

SeekScanVidAI is a comprehensive script designed to streamline the process of extracting audio from videos, transcribing this audio content, and subsequently extracting topics from the transcribed audio. This tool leverages modules such as `extract_audio`, `transcribe_audio_vosk`, and `topic_extraction` to accomplish these tasks.

## Features

- **Audio Extraction**: Extracts the audio from a given video file.
- **Audio Transcription**: Transcribes the extracted audio using the Vosk library.
- **Topic Extraction**: Analyzes the transcribed audio and extracts main topics.

## Usage

To use the script, you need to provide the path to the video, the desired name for the extracted audio file, and optionally the language of the audio (either 'en' or 'pt').

```bash
python run.py <video_path> <audio_name> [--language <either 'en' or 'pt'>]
```

---

## Getting Started

### 1. Clone the Repository:

- Clone the repository to your local machine:

```bash
git clone https://github.com/renan-siqueira/SeekScanVidAI.git
```

- Navigate to the cloned repository:

```bash
cd SeekScanVidAI
```

---

### 2. Set Up a Virtual Environment:

It's recommended to use a virtual environment to avoid package conflicts.
To set it up:

- Install virtualenv if you haven't:

```bash
pip install virtualenv
```

- Create a virtual environment:

```bash
virtualenv venv
```

- Activate the virtual environment:

**On Windows:**

```bash
.\venv\Scripts\activate
```

**On MacOS and Linux:**

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies:

With the virtual environment activated, install the necessary dependencies:

```bash
pip install -r requirements.txt
```

---

## Note:

This script is part of a larger project structure and might be expanded in the future to incorporate more functionalities or to be integrated with other modules.

---

## Contributions
Feel free to contribute, raise issues, or suggest enhancements to improve the project.
