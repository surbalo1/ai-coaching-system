import asyncio
from app.agents.crm_agent import CRMAgent
from app.core.llm import get_openai_client, get_model_name
from app.core.settings import get_settings

async def debug_config():
    settings = get_settings()
    client = get_openai_client()
    print(f"DEBUG ENV KEY: {settings.OPENAI_API_KEY[:10]}...")
    print(f"DEBUG CLIENT BASE URL: {client.base_url}")
    print(f"DEBUG MODEL: {get_model_name()}")
    
    agent = CRMAgent()
    note_action = "Great call with John. He's interested. Please send him the pricing PDF."
    try:
        await agent.analyze_note(note_action, "John Doe")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(debug_config())
