from app.core.llm import get_openai_client, get_model_name
from app.core.models_crm import CRMAction
import json

class CRMAgent:
    def __init__(self):
        self.client = get_openai_client()

    async def analyze_note(self, note_text: str, contact_name: str) -> CRMAction:
        """
        Analyzes a CRM note to determine if an automated follow-up is needed.
        """
        prompt = f"""
        You are a Sales Assistant AI. Analyze the following CRM note written by a salesperson about a call with {contact_name}.
        Determine if an IMMEDIATE follow-up email is needed.

        Intent Categories:
        - "send_email": If the note implies sending info, pricing, links, or a follow-up summary.
        - "none": If it's just a status update (e.g., "Left voicemail", "Not interested").
        
        If intent is "send_email", draft the email subject and body.

        Note: "{note_text}"

        Output JSON:
        {{
            "intent": "send_email" | "none",
            "confidence": 0.9,
            "reason": "Salesperson explicitly asked to send pricing.",
            "email_subject": "Here is the pricing...",
            "email_body": "Hi {contact_name}, ..."
        }}
        """

        try:
            response = await self.client.chat.completions.create(
                model=get_model_name(),
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            data = json.loads(content)
            
            return CRMAction(**data)

        except Exception as e:
            print(f"CRM Analysis Error: {e}")
            return CRMAction(intent="none", confidence=0.0, reason=f"Error: {e}")
