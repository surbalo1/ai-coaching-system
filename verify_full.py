import asyncio
from app.services.rss import RSSService
from app.agents.extractor import ExtractorAgent
from app.agents.outreach import OutreachAgent
from app.services.email import ConsoleEmailService
import sys

# Windows/Event loop policy fix if needed, but for Mac usually fine.

async def main():
    print("🚀 Starting Module A Full Test")
    
    rss = RSSService()
    extractor = ExtractorAgent()
    outreach = OutreachAgent()
    email_service = ConsoleEmailService()
    
    # Using a known podcast
    feed_url = "https://feeds.simplecast.com/vPwtSKsm" # Lenny's Podcast
    episodes = rss.parse_feed(feed_url, days_lookback=30)
    
    if not episodes:
        print("❌ No episodes found to test.")
        return

    # Just take the first one for the test to save tokens/time
    episode = episodes[0] 
    print(f"Processing latest episode: {episode.title}")
    
    print("running extraction...")
    lead = await extractor.extract_guest_info(episode)
    
    if not lead:
        print("❌ Could not extract lead (or returned null).")
        return
        
    print(f"✅ Extracted Lead: {lead.guest.name} (Score: {lead.score})")
    
    print("Generating Email...")
    body = await outreach.generate_email(lead)
    
    await email_service.send_email(
        to_email="test@example.com",
        subject="Test Subject",
        body=body
    )
    
    print("✅ Test Complete")

if __name__ == "__main__":
    asyncio.run(main())
