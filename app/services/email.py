from typing import Protocol
from app.core.models import Lead

class EmailProvider(Protocol):
    async def send_email(self, to_email: str, subject: str, body: str) -> bool:
        ...

class ConsoleEmailService:
    """
    Mock email service that prints to console.
    Use this for dev/testing to avoid spamming real people.
    """
    async def send_email(self, to_email: str, subject: str, body: str) -> bool:
        print(f"--- SIMULATING EMAIL SENDING ---")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}")
        print(f"--------------------------------")
        return True

# Placeholder for real Gmail Implementation
class GmailService:
    async def send_email(self, to_email: str, subject: str, body: str) -> bool:
        # TODO: Implement Gmail API Oauth
        pass
