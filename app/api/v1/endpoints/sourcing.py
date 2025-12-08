from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from app.services.rss import RSSService
from app.agents.extractor import ExtractorAgent
from app.agents.outreach import OutreachAgent
from app.services.email import ConsoleEmailService
from app.core.models import Lead, PodcastEpisode

router = APIRouter()
rss_service = RSSService()
extractor_agent = ExtractorAgent()
outreach_agent = OutreachAgent()
email_service = ConsoleEmailService()

# In-memory storage for demo purposes (replace with DB later)
LEADS_DB: List[Lead] = []

@router.post("/run", response_model=dict)
async def run_sourcing_pipeline(feed_url: str, background_tasks: BackgroundTasks):
    """
    Trigger the sourcing pipeline for a specific RSS feed URL.
    Runs in background to avoid timeout.
    """
    background_tasks.add_task(process_feed, feed_url)
    return {"status": "Pipeline started", "feed_url": feed_url}

@router.get("/leads", response_model=List[Lead])
async def get_leads():
    """
    Get all extracted leads.
    """
    return LEADS_DB

async def process_feed(feed_url: str):
    print(f"Starting processing for {feed_url}")
    # Reduce lookback to avoid processing too many older episodes during tests
    episodes = rss_service.parse_feed(feed_url, days_lookback=14) 
    print(f"Found {len(episodes)} recent episodes")
    
    for episode in episodes:
        lead = await extractor_agent.extract_guest_info(episode)
        
        # Threshold for contacting
        if lead and lead.score >= 7:
            print(f"✅ Found Qualified Lead: {lead.guest.name} (Score: {lead.score})")
            
            # Simple dedup check
            if not any(l.guest.name == lead.guest.name for l in LEADS_DB):
                LEADS_DB.append(lead)
                
                # GEN & SEND EMAIL
                print(f"📧 Generating email for {lead.guest.name}...")
                email_body = await outreach_agent.generate_email(lead)
                
                await email_service.send_email(
                    to_email="test@example.com", # Placeholder
                    subject=f"Quick question re: {episode.title}",
                    body=email_body
                )
        elif lead:
            print(f"Skipping Lead: {lead.guest.name} (Score: {lead.score})")
