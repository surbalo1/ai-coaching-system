import json
from app.core.models import GuestProfile, Lead, LeadStatus, PodcastEpisode
from app.core.llm import get_openai_client, get_model_name
from pydantic import ValidationError

class ExtractorAgent:
    def __init__(self):
        self.client = get_openai_client()

    async def extract_guest_info(self, episode: PodcastEpisode) -> Lead:
        """
        Extracts guest information from episode show notes using LLM.
        """
        prompt = f"""
        You are an expert Data Extractor. simple analyze the following podcast show notes and extract the guest's information.
        
        Rules:
        1. Extract the MAIN guest name. If there are multiple, pick the primary one. If no guest, return null.
        2. Infer the company they work for and their role if mentioned.
        3. Rate the lead from 1-10 (Score) based on relevance to "AI, Entrepreneurship, Coaching".
        4. Return valid JSON only.

        Show Notes:
        {episode.show_notes[:3000]}  # Truncate to save tokens if needed
        
        Output Format (JSON):
        {{
            "name": "First Last",
            "company": "Company Name",
            "role": "CEO/Founder",
            "website": "https://example.com",
            "score": 8,
            "score_reason": "Guest is an AI founder..."
        }}
        """

        try:
            response = await self.client.chat.completions.create(
                model=get_model_name(),
                messages=[{"role": "system", "content": "You are a JSON extractor."},
                          {"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            data = json.loads(content)
            
            # Skip if no name found
            if not data.get('name') or data.get('name').lower() == 'null':
                return None

            guest = GuestProfile(
                name=data.get('name'),
                company=data.get('company'),
                role=data.get('role'),
                website=data.get('website')
            )
            
            return Lead(
                guest=guest,
                episode_context=episode,
                score=data.get('score', 0),
                score_reason=data.get('score_reason'),
                status=LeadStatus.NEW
            )

        except Exception as e:
            print(f"Extraction Error: {e}")
            return None
