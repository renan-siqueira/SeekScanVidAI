"""
Module to extract audio from a given video file using ffmpeg.
"""
import sys
import subprocess


def extract_audio_from_video(video_path: str, output_audio_path: str) -> None:
    """
    Extract audio from a given video file using ffmpeg.
    
    Parameters:
    - video_path: Path to the input video file.
    - output_audio_path: Path where the extracted audio will be saved. Default is "output.wav".
    """
    command: list = [
        'ffmpeg',
        '-i', video_path,
        '-ac', '1', # Mono output
        '-vn', # Don't need video output
        '-acodec', 'pcm_s16le', # Sets the audio codec to pcm_s16le
        '-ar', '16000', # Sets the sample rate to 16000
        output_audio_path
    ]

    subprocess.run(command, check=True)


def get_audio_output_name(file_name: str) -> str:
    """
    Returns the audio output name, appending ".wav" if no extension is provided.
    """
    return file_name + '.wav' if not file_name.endswith('.wav') else file_name


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please provide the video file path and the output audio name.')
        sys.exit(1)

    VIDEO_PATH = sys.argv[1]
    AUDIO_NAME = get_audio_output_name(sys.argv[2])

    extract_audio_from_video(VIDEO_PATH, AUDIO_NAME)
    print(f'Audio extracted to: {AUDIO_NAME}')
