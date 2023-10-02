"""
Test module for the functionality in src.modules.extract_audio.
"""
import sys
import os
import unittest
from unittest.mock import patch, Mock

from src.modules import extract_audio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestExtractAudio(unittest.TestCase):
    """
    Test case class for extract_audio functionalities.
    """
    @patch('src.modules.extract_audio.subprocess.run')
    def test_extract_audio_from_video(self, mock_run: Mock) -> None:
        """
        Test if the extract_audio_from_video function calls subprocess.run with the correct 
        arguments.
        """
        video_path: str = 'input_video.mp4'
        audio_path: str = 'output_audio.wav'

        extract_audio.extract_audio_from_video(video_path, audio_path)

        expected_command: list = [
            'ffmpeg',
            '-i', video_path,
            '-ac', '1',
            '-vn',
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            audio_path
        ]

        mock_run.assert_called_once_with(expected_command, check=True)

    def test_get_audio_output_name(self) -> None:
        """
        Test if the get_audio_output_name function produces the correct output for given inputs.
        """
        self.assertEqual(extract_audio.get_audio_output_name('audio'), 'audio.wav')
        self.assertEqual(extract_audio.get_audio_output_name('audio.wav'), 'audio.wav')
        self.assertEqual(extract_audio.get_audio_output_name('my.audio'), 'my.audio.wav')


if __name__ == '__main__':
    unittest.main()
