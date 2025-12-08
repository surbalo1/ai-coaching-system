import asyncio
from app.agents.crm_agent import CRMAgent
from app.core.models_crm import CRMAction

async def test_crm_analysis():
    print("🤖 Testing CRM Agent Analysis...")
    agent = CRMAgent()
    
    # Test Case 1: Action Required
    note_action = "Great call with John. He's interested. Please send him the pricing PDF and the case study link."
    print(f"\n📝 Analyzing Note 1: '{note_action}'")
    
    action1 = await agent.analyze_note(note_action, "John Doe")
    print(f"   -> Intent: {action1.intent}")
    print(f"   -> Confidence: {action1.confidence}")
    if action1.intent == "send_email":
        print(f"   -> Subject: {action1.email_subject}")
        print(f"   -> Body Preview: {action1.email_body[:50]}...")
    
    # Test Case 2: No Action
    note_noise = "Left a voicemail. Will try again next week."
    print(f"\n📝 Analyzing Note 2: '{note_noise}'")
    
    action2 = await agent.analyze_note(note_noise, "Jane Doe")
    print(f"   -> Intent: {action2.intent}")
    
    if action1.intent == "send_email" and action2.intent == "none":
        print("\n✅ VERIFICATION SUCCESS: Agent correctly identified intents.")
    else:
        print("\n❌ VERIFICATION FAILED: Intents mismatch.")

if __name__ == "__main__":
    asyncio.run(test_crm_analysis())
