from app.core.models_outreach import Prospect, ProspectStatus
import random

class EnrichmentService:
    async def enrich_prospect(self, prospect: Prospect) -> Prospect:
        """
        Mock enrichment service. In prod, this would call Apollo/Hunter API.
        """
        print(f"🔎 Enriching {prospect.email}...")
        
        # Simulate API latency
        # await asyncio.sleep(1)
        
        # Mock finding data randomly
        found = random.choice([True, True, False]) # 66% find rate
        
        if found:
            prospect.company = prospect.company or "Tech Innovators Inc."
            prospect.linkedin_url = f"https://linkedin.com/in/{prospect.first_name.lower()}-{prospect.last_name.lower()}" if prospect.last_name else None
            prospect.enrichment_data = {
                "industry": "Artificial Intelligence",
                "employee_count": "11-50",
                "location": "San Francisco, CA"
            }
            prospect.status = ProspectStatus.ENRICHED
            print(f"✅ Found data for {prospect.email}")
        else:
            print(f"⚠️ No extra data found for {prospect.email}")
        
        return prospect
