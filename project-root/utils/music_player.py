import asyncio
import subprocess

class MusicPlayer:
    """Represents a music player that handles decoding and streaming audio."""

    def __init__(self, source: str):
        """
        Initializes the MusicPlayer with the audio source.

        Args:
            source: The URL or file path of the audio source.
        """
        self.source = source
        self.ffmpeg = None

    async def play_song(self):
        """
        Starts playing the audio using FFmpeg.

        Raises:
            subprocess.CalledProcessError: If FFmpeg encounters an error.
        """
        if self.ffmpeg is not None:
            await self.stop()

        self.ffmpeg = await asyncio.create_subprocess_exec(
            'ffmpeg',
            '-i', self.source,
            '-vn',  # Disable video output
            '-f', 's16le',  # 16-bit signed little-endian output
            '-ar', '48000',  # Sample rate 48 kHz
            '-ac', '2',  # 2 channels (stereo)
            'pipe:1',  # Output to pipe
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    async def stop(self):
        """Stops the FFmpeg process and cleans up."""
        if self.ffmpeg is not None:
            self.ffmpeg.terminate()
            await self.ffmpeg.wait()
            self.ffmpeg = None