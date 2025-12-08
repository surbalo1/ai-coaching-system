from app.services.rss import RSSService
import json

def test_rss():
    service = RSSService()
    # Using a popular podcast about AI/Tech as a test
    feed_url = "https://feeds.simplecast.com/vPwtSKsm" # Lenny's Podcast
    
    print(f"Testing feed: {feed_url}")
    episodes = service.parse_feed(feed_url, days_lookback=30) # Look back 30 days to ensure we get something
    
    print(f"Found {len(episodes)} episodes.")
    
    if episodes:
        print("\nLast Episode found:")
        ep = episodes[0]
        print(f"Title: {ep.title}")
        print(f"Date: {ep.published_date}")
        print(f"Audio: {ep.audio_url}")
        print(f"Summary preview: {ep.show_notes[:100]}...")
    else:
        print("No episodes found. (Check network or days_lookback)")

if __name__ == "__main__":
    test_rss()
