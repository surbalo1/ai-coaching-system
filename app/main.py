from fastapi import FastAPI
from app.core.settings import get_settings

settings = get_settings()

from app.core.database import create_db_and_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load DB
    create_db_and_tables()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend AI Automation System for Coaching Company",
    lifespan=lifespan
)

from fastapi.middleware.cors import CORSMiddleware

# CORS (Backend Security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, set to specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.v1.endpoints import sourcing, coach, media, outreach, crm, twin

app.include_router(sourcing.router, prefix="/api/v1/sourcing", tags=["sourcing"])
app.include_router(coach.router, prefix="/api/v1/coach", tags=["coach"])
app.include_router(media.router, prefix="/api/v1/media", tags=["media"])
app.include_router(outreach.router, prefix="/api/v1/outreach", tags=["outreach"])
app.include_router(crm.router, prefix="/api/v1/crm", tags=["crm"])
app.include_router(twin.router, prefix="/api/v1/twin", tags=["twin"]) # New Digital Twin

@app.get("/")
async def root():
    return {
        "message": "System Operational",
        "doc_url": "/docs",
        "environment": settings.ENVIRONMENT
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}
