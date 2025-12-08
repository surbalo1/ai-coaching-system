from fastapi import APIRouter, UploadFile, File
from app.services.rag_service import RAGService
from app.core.models_rag import QueryRequest, QueryResponse
from app.core.llm import get_openai_client, get_model_name
import shutil
import os

router = APIRouter()
rag_service = RAGService()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a text file to the Knowledge Base.
    """
    # Save temp
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Read content (Assuming text file for V1, add PDF logic later)
    try:
        with open(temp_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        rag_service.ingest_text(content, file.filename)
        
        return {"status": "Ingested", "filename": file.filename}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/ask", response_model=QueryResponse)
async def ask_coach(request: QueryRequest):
    """
    RAG Endpoint: Retrieve context -> Send to GPT -> Answer.
    """
    # 1. Retrieve
    relevant_chunks = rag_service.search(request.query, limit=request.limit)
    context_str = "\n\n".join(relevant_chunks)
    
    # 2. Generate
    client = get_openai_client()
    
    prompt = f"""
    You are an AI Coach for a high-end business coaching program.
    Answer the user's question based ONLY on the following Context. 
    If the answer is not in the context, say "I don't have that info in my knowledge base."

    Context:
    {context_str}

    Question:
    {request.query}
    """
    
    response = await client.chat.completions.create(
        model=get_model_name(),
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = response.choices[0].message.content
    
    return QueryResponse(
        answer=answer,
        sources=relevant_chunks
    )
