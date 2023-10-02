import sys
import subprocess


def extract_audio_from_video(video_path, output_audio_path="output.wav"):
    command = [
        'ffmpeg',
        '-i', video_path,
        '-ac', '1', # Mono output
        '-vn', # Don't need video output
        '-acodec', 'pcm_s16le', # Sets the audio codec to pcm_s16le
        '-ar', '16000', # Sets the sample rate to 16000
        output_audio_path
    ]

    subprocess.run(command)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide the video file path.')
        sys.exit(1)

    VIDEO_PATH = sys.argv[1]
    AUDIO_NAME = sys.argv[2] + '.wav'

    extract_audio_from_video(VIDEO_PATH, AUDIO_NAME)
    print(f'Audio extracted to: {AUDIO_NAME}')
