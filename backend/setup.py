"""
Setup script for RAMate backend.
Initializes the system by processing PDFs and creating the vector store.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from parse_pdfs import PDFProcessor
from embed_and_store import EmbeddingManager

def setup_ramate():
    """Complete setup of RAMate backend system."""
    
    print("🚀 Setting up RAMate Backend System...")
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration
    pdf_dir = os.getenv('PDF_DIRECTORY', '../pdfs')
    chroma_path = os.getenv('CHROMA_DB_PATH', '../chroma_store')
    chunk_size = int(os.getenv('CHUNK_SIZE', 500))
    chunk_overlap = int(os.getenv('CHUNK_OVERLAP', 50))
    
    print(f"📁 PDF Directory: {pdf_dir}")
    print(f"🗂️  ChromaDB Path: {chroma_path}")
    print(f"📄 Chunk Size: {chunk_size}")
    print(f"🔗 Chunk Overlap: {chunk_overlap}")
    
    # Check if PDFs exist
    pdf_path = Path(pdf_dir)
    if not pdf_path.exists():
        print(f"❌ Error: PDF directory not found: {pdf_path}")
        return False
    
    pdf_files = list(pdf_path.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ Error: No PDF files found in {pdf_path}")
        return False
    
    print(f"📚 Found {len(pdf_files)} PDF files:")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file.name}")
    
    try:
        # Step 1: Initialize PDF processor
        print("\n📄 Step 1: Initializing PDF processor...")
        pdf_processor = PDFProcessor(
            pdf_directory=pdf_dir,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        # Step 2: Process PDFs
        print("\n🔍 Step 2: Processing PDF documents...")
        chunks = pdf_processor.process_all_pdfs()
        
        if not chunks:
            print("❌ Error: No chunks were created from PDFs")
            return False
        
        print(f"✅ Created {len(chunks)} text chunks")
        
        # Step 3: Initialize embedding manager
        print("\n🧠 Step 3: Initializing embedding manager...")
        embedding_manager = EmbeddingManager(chroma_db_path=chroma_path)
        
        # Check if collection already has data
        stats = embedding_manager.get_collection_stats()
        if stats.get('total_chunks', 0) > 0:
            print(f"⚠️  Found existing data: {stats['total_chunks']} chunks")
            response = input("Clear existing data and rebuild? (y/N): ").strip().lower()
            if response != 'y':
                print("Setup cancelled by user")
                return False
            embedding_manager.clear_collection()
        
        # Step 4: Generate embeddings and store
        print("\n🔗 Step 4: Generating embeddings and storing in vector database...")
        
        # Use local embeddings for initial setup (can be changed later)
        embedding_manager.add_documents(chunks, use_openrouter=False)
        
        # Step 5: Verify setup
        print("\n✅ Step 5: Verifying setup...")
        final_stats = embedding_manager.get_collection_stats()
        
        print(f"📊 Setup Complete!")
        print(f"  - Total chunks in vector store: {final_stats['total_chunks']}")
        print(f"  - Source documents: {final_stats['unique_sources']}")
        print(f"  - Source files: {', '.join(final_stats['source_files'])}")
        
        # Test a sample query
        print("\n🔍 Testing with sample query...")
        from rag_engine import RAGEngine
        
        rag_engine = RAGEngine(chroma_db_path=chroma_path)
        test_result = rag_engine.answer_question("What are emergency procedures?")
        
        print(f"Sample query confidence: {test_result['confidence']:.3f}")
        print(f"Sources found: {len(test_result['sources'])}")
        
        print("\n🎉 RAMate backend setup completed successfully!")
        print("\nNext steps:")
        print("1. Configure your OpenRouter API key in .env for enhanced responses")
        print("2. Run 'python app.py' to start the Flask API server")
        print("3. Set up the frontend to connect to your API")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during setup: {str(e)}")
        return False

def main():
    """Main function."""
    success = setup_ramate()
    
    if not success:
        print("\n❌ Setup failed. Please check the errors above and try again.")
        sys.exit(1)
    else:
        print("\n✅ Setup completed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()
