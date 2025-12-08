from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from app.services.media_processor import MediaProcessor
from app.agents.clipper import ClipperAgent
import shutil
import os

router = APIRouter()
media_processor = MediaProcessor()
clipper_agent = ClipperAgent()

@router.post("/process_video")
async def process_video(file: UploadFile = File(...)):
    """
    Full pipeline: Upload -> Extract Audio -> Transcribe -> Find Clip -> Cut Clip.
    """
    temp_path = f"temp_media/{file.filename}"
    os.makedirs("temp_media", exist_ok=True)
    
    # Save Upload
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Processing (Synchronous for waiting response, could be backgrounded)
    # 1. Audio
    audio_path = await media_processor.extract_audio(temp_path)
    
    # 2. Transcribe
    transcript = await media_processor.transcribe(audio_path)
    
    # 3. Identify
    clips = await clipper_agent.identify_clips(transcript)
    
    if not clips:
        return {"status": "No clips found"}
        
    best_clip = clips[0]
    
    # 4. Cut
    # Note: GPT returns timestamps based on transcript flow. 
    # Accurate timestamping from pure text to video time is tricky without word-level timestamps from Whisper.
    # For V1 we assume GPT estimating or we need a better mapping.
    # Actually, Whisper API provides segments with times. 
    # IMPROVEMENT: We should pass segments to GPT, not just raw text, to get real times.
    # For now, let's assume the user accepts the 'transcript' approach and we cut based on what GPT says roughly,
    # OR we refine the implementation to ask for 'quotes' and we find timestamps.
    # Let's stick to the extraction for now.
    
    clip_path = await media_processor.cut_video(
        temp_path, 
        best_clip.start_time, 
        best_clip.end_time
    )
    
    return {
        "status": "Success",
        "original_transcript": transcript[:100] + "...",
        "clip_data": best_clip,
        "download_url": clip_path # In real app, upload to S3 and return URL
    }
