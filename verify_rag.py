from app.services.rag_service import RAGService
import time

def test_rag():
    print("Initializing RAG Service...")
    try:
        service = RAGService()
    except Exception as e:
        print(f"Error initializing: {e}")
        return

    # 1. Ingest
    filename = "manual_test.txt"
    text = """
    The Coaching Company offers a 10K High-Ticket Program.
    This program includes weekly Q&A calls with the founders.
    It focuses on AI systems and automation for business growth.
    """
    
    print(f"Ingesting text from {filename}...")
    try:
        service.ingest_text(text, filename)
    except Exception as e:
        print(f"Error ingesting: {e}")
        return

    # 2. Search
    query = "Does the program include weekly calls?"
    print(f"Searching for: '{query}'")
    
    try:
        results = service.search(query, limit=1)
        print(f"Found {len(results)} chunks.")
        for r in results:
            print(f"--- Chunk ---\n{r}\n-----------")
            
        if "weekly Q&A calls" in results[0]:
            print("✅ VERIFICATION SUCCESS: Retrieved correct context.")
        else:
            print("❌ VERIFICATION FAILED: Did not retrieve expected context.")
            
    except Exception as e:
        print(f"Error searching: {e}")

if __name__ == "__main__":
    test_rag()
