from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from enum import Enum
import datetime

class CRMContact(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None

class WebhookType(str, Enum):
    CONTACT_UPDATED = "ContactUpdated"
    NOTE_ADDED = "NoteAdded"
    TAG_ADDED = "TagAdded"

class WebhookPayload(BaseModel):
    type: WebhookType
    contact: CRMContact
    data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)

class CRMAction(BaseModel):
    intent: str  # "send_email", "schedule_task", "none"
    confidence: float
    email_subject: Optional[str] = None
    email_body: Optional[str] = None
    reason: str
