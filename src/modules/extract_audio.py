"""
Module to extract audio from a given video file using ffmpeg.
"""
import os
import subprocess


def extract_audio_from_video(
        video_path: str,
        output_audio_path: str,
        acodec: str ='pcm_s16le',
        sample_rate: str='16000'
    ) -> None:
    """
    Extract audio from a given video file using ffmpeg.
    
    Parameters:
    - video_path: Path to the input video file.
    - output_audio_path: Path where the extracted audio will be saved.
    - acodec: Audio codec to use. Default is 'pcm_s16le'.
    - sample_rate: Sample rate to use. Default is '16000'.
    """
    command: list = [
        'ffmpeg',
        '-i', video_path,
        '-ac', '1',
        '-vn',
        '-acodec', acodec,
        '-ar', sample_rate,
        output_audio_path
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to extract audio from {video_path}")
        raise


def get_audio_output_name(file_name: str) -> str:
    """
    Returns the audio output name, appending ".wav" if no extension is provided.
    """
    return file_name + '.wav' if not file_name.endswith('.wav') else file_name


def main(video_path: str, audio_name: str, audio_path: str):
    """Main function to handle the audio extraction process."""
    audio_output = get_audio_output_name(audio_name)
    audio_output_path = os.path.join(audio_path, audio_output)

    extract_audio_from_video(video_path, audio_output_path)
    print(f'Audio extracted to: {audio_output_path}')

    return audio_output_path
