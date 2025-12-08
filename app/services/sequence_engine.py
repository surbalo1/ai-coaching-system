from app.core.models_outreach import Campaign, Prospect, ProspectStatus
from app.services.enrichment import EnrichmentService
from app.services.email import ConsoleEmailService
from app.agents.outreach import OutreachAgent
from datetime import datetime, timedelta
from typing import List

class SequenceEngine:
    def __init__(self):
        self.enrichment = EnrichmentService()
        self.email_service = ConsoleEmailService()
        self.agent = OutreachAgent() # Reusing Mod A Agent
        
        # In-memory DBs (Simulating SQL usage)
        self.campaigns = {} # id -> Campaign
        self.prospects = {} # id -> Prospect

    async def add_campaign(self, campaign: Campaign):
        self.campaigns[campaign.id] = campaign
        
    async def add_prospects(self, prospects: List[Prospect]):
        for p in prospects:
            self.prospects[p.id] = p

    async def run_campaign(self, campaign_id: str):
        """
        Main Loop: Checks all prospects in a campaign and advances their state.
        """
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")
            
        print(f"🚀 Running Campaign: {campaign.name}")
        
        # Get prospects for this campaign
        campaign_prospects = [p for p in self.prospects.values() if p.campaign_id == campaign_id]
        
        for prospect in campaign_prospects:
            await self._process_prospect(prospect, campaign)

    async def _process_prospect(self, prospect: Prospect, campaign: Campaign):
        # 1. Enrich if New
        if prospect.status == ProspectStatus.NEW:
            prospect = await self.enrichment.enrich_prospect(prospect)
            
        # 2. Check Sequence Steps
        next_step_num = prospect.step_completed + 1
        
        # Find the step config
        step_config = next(
            (s for s in campaign.steps if s.step_number == next_step_num), 
            None
        )
        
        if not step_config:
            # End of sequence
            return

        # 3. Check Timing
        if prospect.last_contacted_at:
            delta = datetime.now() - prospect.last_contacted_at
            if delta.days < step_config.day_delay:
                # Too soon
                return

        # 4. Generate & Send
        print(f"📧 Sending Step {next_step_num} to {prospect.email}...")
        
        # Use simple prompt logic here, or full OutreachAgent if we have context
        # For simplicity in V1, we construct a prompt based on the template
        body = f"Subject: Hello\n\n[ AI Generated Body based on: {step_config.prompt_template} ]" 
        
        # In a real app, we'd call self.agent.generate_with_prompt(step_config.prompt_template, prospect)
        
        await self.email_service.send_email(
            to_email=prospect.email,
            subject=f"Campaign Msg {next_step_num}",
            body=body
        )
        
        # 5. Update State
        prospect.status = ProspectStatus.CONTACTED
        prospect.last_contacted_at = datetime.now()
        prospect.step_completed = next_step_num
