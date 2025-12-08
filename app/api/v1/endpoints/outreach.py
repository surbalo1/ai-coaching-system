from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.sequence_engine import SequenceEngine
from app.core.models_outreach import Campaign, Prospect, SequenceStep
from typing import List

router = APIRouter()
engine = SequenceEngine() # Singleton logic for demo

@router.post("/campaigns", response_model=Campaign)
async def create_campaign(name: str, objective: str):
    """
    Create a new outreach campaign with default 2-step sequence.
    """
    steps = [
        SequenceStep(step_number=1, day_delay=0, prompt_template="Intro email about " + objective),
        SequenceStep(step_number=2, day_delay=3, prompt_template="Follow up on previous email")
    ]
    
    start_campaign = Campaign(name=name, description=objective, steps=steps)
    await engine.add_campaign(start_campaign)
    return start_campaign

@router.post("/upload_prospects")
async def upload_prospects(campaign_id: str, emails: List[str]):
    """
    Simple bulk add of prospects (email only) to a campaign.
    """
    new_prospects = []
    for email in emails:
        p = Prospect(
            campaign_id=campaign_id, 
            email=email, 
            first_name=email.split("@")[0] # Naive parsing
        )
        new_prospects.append(p)
        
    await engine.add_prospects(new_prospects)
    return {"status": "Added", "count": len(new_prospects)}

@router.post("/run/{campaign_id}")
async def run_campaign(campaign_id: str, background_tasks: BackgroundTasks):
    """
    Trigger the sequence engine for a campaign.
    """
    background_tasks.add_task(engine.run_campaign, campaign_id)
    return {"status": "Running", "campaign_id": campaign_id}
