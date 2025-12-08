from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.llm import get_openai_client, get_model_name

router = APIRouter()

class TwinRequest(BaseModel):
    message: str
    sender_id: str = "anonymous"
    channel: str = "generic" # whatsapp, telegram, web

class TwinResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=TwinResponse)
async def chat_with_twin(request: TwinRequest):
    """
    Simplified Endpoint for External Bots (WhatsApp/Telegram).
    No complex JSON structures, just text-in -> text-out.
    """
    client = get_openai_client()
    model = get_model_name()
    
    # 1. Build Context (In V2, retrieval tailored to short messages)
    # For now, we use a concise persona.
    system_prompt = (
        "You are the Digital Twin of a high-performance Executive Coach. "
        "You are chatting on a messaging app (WhatsApp/Telegram), so keep your responses "
        "concise, punchy, and engaging. No long paragraphs. Use emojis sparingly. "
        "Focus on immediate value."
    )

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            max_tokens=300 # Keep it short for mobile
        )
        
        reply_text = response.choices[0].message.content
        return TwinResponse(reply=reply_text)

    except Exception as e:
        print(f"Twin Error: {e}")
        raise HTTPException(status_code=500, detail="Coach is offline temporarily.")
