from openai import AsyncOpenAI
from app.core.models import Lead, GuestProfile, PodcastEpisode
from app.core.settings import get_settings
from app.core.llm import get_model_name

class OutreachAgent:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=get_settings().OPENAI_API_KEY)

    async def generate_email(self, lead: Lead) -> str:
        """
        Generates a hyper-personalized cold email for a podcast guest.
        """
        guest = lead.guest
        episode = lead.episode_context
        
        prompt = f"""
        You are an expert copywriter for a high-ticket coaching business.
        Write a SHORT, personalized email to {guest.name} inviting them to chat about a potential collaboration or summit.
        
        Context:
        - They just appeared on the "{episode.podcast_name}" podcast.
        - Episode Title: "{episode.title}"
        - We act as an "AI Systems Partner".
        
        Rules:
        1. Subject Line: casual but relevant (e.g., "Loved your episode on {episode.podcast_name}")
        2. Opening: Mention a specific insightful thing they might have said based on the episode topic: "{episode.title}"
        3. The Ask: A brief 15-min chat to trade notes on AI systems (soft sell).
        4. Tone: Professional, peer-to-peer, not salesy.
        
        Return ONLY the email body. Subject line on the first line prefixed with "Subject: ".
        """

        try:
            response = await self.client.chat.completions.create(
                model=get_model_name(),
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating email: {e}"
