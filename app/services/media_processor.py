import subprocess
import os
from app.core.settings import get_settings
from app.core.llm import get_openai_client
import asyncio

settings = get_settings()

class MediaProcessor:
    def __init__(self):
        self.tmp_dir = "temp_media"
        os.makedirs(self.tmp_dir, exist_ok=True)

    async def extract_audio(self, video_path: str) -> str:
        """
        Extracts audio from video using FFmpeg. Returns path to .mp3
        """
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_path = os.path.join(self.tmp_dir, f"{base_name}.mp3")
        
        # FFmpeg command: -y (overwrite), -i input, -vn (no video), -acodec mp3
        cmd = [
            "ffmpeg", "-y", 
            "-i", video_path, 
            "-vn", 
            "-acodec", "libmp3lame", 
            output_path
        ]
        
        print(f"Running FFmpeg: {' '.join(cmd)}")
        
        # Run properly allowing for async roughly
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            print(f"FFmpeg Error: {stderr.decode()}")
            raise Exception("FFmpeg extraction failed")
            
        return output_path

    async def transcribe(self, audio_path: str) -> str:
        """
        Transcribes audio using OpenAI Whisper-1 model.
        """
        client = get_openai_client()
        
        with open(audio_path, "rb") as audio_file:
            transcript = await client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        
        return transcript.text

    async def cut_video(self, video_path: str, start_time: str, end_time: str, output_suffix: str = "clip") -> str:
        """
        Cuts a clip from video using FFmpeg. Times in HH:MM:SS or seconds.
        """
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_path = os.path.join(self.tmp_dir, f"{base_name}_{output_suffix}.mp4")
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-ss", str(start_time),
            "-to", str(end_time),
            "-c", "copy", # Fast cut (might be slightly inaccurate on keyframes, but fast)
            output_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
             # Try re-encoding if copy fails or is weird
             cmd[6] = "libx264" # remove -c copy
             
             raise Exception(f"Cut failed: {stderr.decode()}")
             
        return output_path
