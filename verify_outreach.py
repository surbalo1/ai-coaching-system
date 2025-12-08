import asyncio
from app.services.sequence_engine import SequenceEngine
from app.core.models_outreach import Campaign, Prospect, SequenceStep, ProspectStatus
from datetime import datetime, timedelta

async def test_outreach():
    engine = SequenceEngine()
    
    # 1. Setup Campaign
    print("🔧 Setting up Campaign...")
    steps = [
        SequenceStep(step_number=1, day_delay=0, prompt_template="Intro email"),
        SequenceStep(step_number=2, day_delay=2, prompt_template="Follow up")
    ]
    campaign = Campaign(name="Test Campaign", steps=steps)
    await engine.add_campaign(campaign)
    
    # 2. Add Prospect
    prospect = Prospect(
        campaign_id=campaign.id,
        email="ceo@techstart.up",
        first_name="Elon"
    )
    await engine.add_prospects([prospect])
    
    # 3. First Run (Should send Step 1)
    print("\n🚀 Run 1: Initial Trigger")
    await engine.run_campaign(campaign.id)
    
    # Check
    p = engine.prospects[prospect.id]
    if p.step_completed == 1 and p.status == ProspectStatus.CONTACTED:
        print("✅ Step 1 Sent Successfully.")
    else:
        print(f"❌ Step 1 Failed. Status: {p.status}, Step: {p.step_completed}")
        return

    # 4. Immediate Second Run (Should NOT send Step 2 due to delay)
    print("\n🚀 Run 2: Immediate Re-run (Should skip)")
    await engine.run_campaign(campaign.id)
    if p.step_completed == 1:
        print("✅ Correctly skipped Step 2 (wait time).")
    else:
        print("❌ Sent Step 2 too early!")
        
    # 5. Simulate Time Travel (3 days later)
    print("\n🚀 Run 3: 3 Days Later (Should send Step 2)")
    # Hack the last_contacted_at
    p.last_contacted_at = datetime.now() - timedelta(days=3)
    
    await engine.run_campaign(campaign.id)
    
    if p.step_completed == 2:
        print("✅ Step 2 Sent Successfully.")
    else:
         print(f"❌ Step 2 Failed. Status: {p.status}, Step: {p.step_completed}")

if __name__ == "__main__":
    asyncio.run(test_outreach())
