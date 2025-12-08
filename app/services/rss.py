import feedparser
from datetime import datetime, timedelta
from typing import List
from dateutil import parser as date_parser
from app.core.models import PodcastEpisode

class RSSService:
    def parse_feed(self, feed_url: str, days_lookback: int = 3) -> List[PodcastEpisode]:
        """
        Parses an RSS feed and returns episodes from the last N days.
        """
        feed = feedparser.parse(feed_url)
        episodes = []
        
        if not feed.entries:
            return []

        podcast_name = feed.feed.get('title', 'Unknown Podcast')
        cutoff_date = datetime.now(datetime.timezone.utc) - timedelta(days=days_lookback)

        for entry in feed.entries:
            # Handle different date formats
            try:
                published_parsed = entry.get('published_parsed') or entry.get('updated_parsed')
                if published_parsed:
                    published_dt = datetime(*published_parsed[:6]).replace(tzinfo=datetime.timezone.utc)
                else:
                    continue # Skip if no date
                
                if published_dt < cutoff_date:
                    continue

                # Find audio link
                audio_url = None
                for link in entry.get('links', []):
                    if link.get('type', '').startswith('audio'):
                        audio_url = link.get('href')
                        break
                
                episode = PodcastEpisode(
                    title=entry.get('title', 'No Title'),
                    podcast_name=podcast_name,
                    published_date=published_dt,
                    audio_url=audio_url,
                    show_notes=entry.get('summary', '') or entry.get('description', ''),
                    guid=entry.get('id', entry.get('link')),
                    duration=entry.get('itunes_duration')
                )
                episodes.append(episode)
                
            except Exception as e:
                print(f"Error parsing entry in {podcast_name}: {e}")
                continue

        return episodes
