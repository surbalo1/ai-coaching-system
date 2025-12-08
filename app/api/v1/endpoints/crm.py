from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.core.models_crm import WebhookPayload, WebhookType
from app.agents.crm_agent import CRMAgent
from app.services.email import ConsoleEmailService

router = APIRouter()
crm_agent = CRMAgent()
email_service = ConsoleEmailService()

@router.post("/webhook")
async def crm_webhook(payload: WebhookPayload, background_tasks: BackgroundTasks):
    """
    Receives events from GoHighLevel (Simulated).
    """
    if payload.type == WebhookType.NOTE_ADDED:
        background_tasks.add_task(process_note_event, payload)
        return {"status": "Processing Note"}
    
    return {"status": "Ignored Event Type"}

async def process_note_event(payload: WebhookPayload):
    note_text = payload.data.get("note", "")
    contact = payload.contact
    
    print(f"📥 Received CRM Note for {contact.name}: {note_text}")
    
    # Analyze
    action = await crm_agent.analyze_note(note_text, contact.name)
    print(f"🤖 AI Analysis: Intent={action.intent} (Confidence={action.confidence})")
    
    if action.intent == "send_email" and action.confidence > 0.8:
        print("🚀 Auto-Executing Follow-up...")
        await email_service.send_email(
            to_email=contact.email,
            subject=action.email_subject,
            body=action.email_body
        )
    else:
        print("⏸️ No action required.")
