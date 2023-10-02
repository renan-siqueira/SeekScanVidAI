import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import unittest
from unittest.mock import patch
from src.modules import extract_audio


class TestExtractAudio(unittest.TestCase):

    @patch('src.modules.extract_audio.subprocess.run')
    def test_extract_audio_from_video(self, mock_run):
        video_path = 'input_video.mp4'
        audio_path = 'output_audio.wav'

        extract_audio.extract_audio_from_video(video_path, audio_path)

        expected_command = [
            'ffmpeg',
            '-i', video_path,
            '-ac', '1',
            '-vn',
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            audio_path
        ]

        mock_run.assert_called_once_with(expected_command, check=True)

        def test_get_audio_output_name(self):
            self.assertEqual(extract_audio.get_audio_output_name('audio'), 'audio.wav')
            self.assertEqual(extract_audio.get_audio_output_name('audio.wav'), 'audio.wav')
            self.assertEqual(extract_audio.get_audio_output_name('my.audio'), 'my.audio.wav')


if __name__ == '__main__':
    unittest.main()
