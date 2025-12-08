from sqlmodel import Session, select
from app.core.database import engine, create_db_and_tables
from app.core.models_outreach import Campaign, Prospect, SequenceStep

def test_db():
    create_db_and_tables()
    
    with Session(engine) as session:
        # Create Campaign
        camp = Campaign(name="DB Test Campaign")
        session.add(camp)
        session.commit()
        session.refresh(camp)
        
        # Add Steps
        step1 = SequenceStep(campaign_id=camp.id, step_number=1, day_delay=0, prompt_template="Hi")
        session.add(step1)
        
        # Add Prospect
        prospect = Prospect(
            campaign_id=camp.id, 
            email="test@db.com", 
            first_name="Test", 
            enrichment_data={"source": "sqlmodel"}
        )
        session.add(prospect)
        session.commit()
        
        # Read Back
        statement = select(Campaign).where(Campaign.name == "DB Test Campaign")
        results = session.exec(statement).first()
        
        if results:
            print(f"✅ DB Success: Retrieve Campaign '{results.name}' with ID {results.id}")
            print(f"   -> Linked Steps: {len(results.steps)}")
            print(f"   -> Linked Prospects: {len(results.prospects)}")
        else:
            print("❌ DB Failure: Campaign not found")

if __name__ == "__main__":
    test_db()
