from sqlmodel import SQLModel, Field, Relationship, JSON
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum
import uuid

class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"

class ProspectStatus(str, Enum):
    NEW = "new"
    ENRICHED = "enriched"
    CONTACTED = "contacted"
    RESPONDED = "responded"
    BOUNCED = "bounced"

# Steps are embedded as JSON in SQLite for V1 simplicity (or separate table if strict normalization needed)
# Using separate table is safer for future editing.

class SequenceStep(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    campaign_id: str = Field(foreign_key="campaign.id")
    step_number: int
    day_delay: int 
    prompt_template: str

    campaign: "Campaign" = Relationship(back_populates="steps")

class Campaign(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    description: Optional[str] = None
    status: CampaignStatus = CampaignStatus.DRAFT
    created_at: datetime = Field(default_factory=datetime.now)
    
    steps: List[SequenceStep] = Relationship(back_populates="campaign")
    prospects: List["Prospect"] = Relationship(back_populates="campaign")

class Prospect(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    campaign_id: str = Field(foreign_key="campaign.id")
    email: str = Field(index=True) # EmailStr not directly supported in SQLModel 0.0.8 types easily without custom types
    first_name: str
    last_name: Optional[str] = None
    company: Optional[str] = None
    linkedin_url: Optional[str] = None
    
    status: ProspectStatus = ProspectStatus.NEW
    last_contacted_at: Optional[datetime] = None
    step_completed: int = 0
    
    enrichment_data: Dict = Field(default={}, sa_type=JSON) 

    campaign: Campaign = Relationship(back_populates="prospects")
