from app.core.llm import get_openai_client, get_model_name
import json
from pydantic import BaseModel

class ClipSuggestion(BaseModel):
    start_time: str
    end_time: str
    reason: str
    viral_score: int

class ClipperAgent:
    def __init__(self):
        self.client = get_openai_client()

    async def identify_clips(self, transcript: str) -> list[ClipSuggestion]:
        """
        Analyzes transcript to find viral clips.
        """
        prompt = f"""
        You are a Viral Content Editor. Analyze the transcription of this video and identify the ONE best clip to post on social media (Shorts/Reels).
        
        Criteria:
        - Hooky start.
        - Standalone value (makes sense without context).
        - Emotional or high-value insight.
        - Length: 30-60 seconds approx (estimate words).
        
        Transcript:
        {transcript[:15000]}... # Truncate if too long

        Output strictly valid JSON:
        {{
            "clips": [
                {{
                    "start_time": "00:00:10",
                    "end_time": "00:00:50",
                    "reason": "Explains the core problem clearly.",
                    "viral_score": 9
                }}
            ]
        }}
        """

        try:
            response = await self.client.chat.completions.create(
                model=get_model_name(),
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            data = json.loads(response.choices[0].message.content)
            clips = []
            for item in data.get('clips', []):
                clips.append(ClipSuggestion(**item))
                
            return clips
        except Exception as e:
            print(f"Clipper Error: {e}")
            return []
