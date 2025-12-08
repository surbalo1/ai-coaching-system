from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class LeadStatus(str, Enum):
    NEW = "new"
    PROCESSING = "processing"
    QUALIFIED = "qualified"
    DISQUALIFIED = "disqualified"
    DM_SENT = "dm_sent"

class PodcastEpisode(BaseModel):
    title: str
    podcast_name: str
    published_date: datetime
    audio_url: Optional[str] = None
    show_notes: str
    duration: Optional[str] = None
    guid: str  # Unique ID for deduplication

class GuestProfile(BaseModel):
    name: str
    company: Optional[str] = None
    role: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None
    website: Optional[HttpUrl] = None
    email: Optional[str] = None

class Lead(BaseModel):
    id: Optional[str] = None
    guest: GuestProfile
    episode_context: PodcastEpisode
    score: int = Field(default=0, ge=0, le=10)
    score_reason: Optional[str] = None
    status: LeadStatus = LeadStatus.NEW
    created_at: datetime = Field(default_factory=datetime.now)
