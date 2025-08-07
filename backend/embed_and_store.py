"""
Embedding and Vector Store Manager for RAMate.
Handles text embeddings and ChromaDB operations for retrieval.
"""

import os
import uuid
from typing import List, Dict, Any, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class EmbeddingManager:
    """Manages text embeddings and vector storage using ChromaDB."""
    
    def __init__(self, chroma_db_path: str = None, collection_name: str = "ramate_docs"):
        """
        Initialize embedding manager with ChromaDB.
        
        Args:
            chroma_db_path: Path to ChromaDB persistent storage
            collection_name: Name of the ChromaDB collection
        """
        self.chroma_db_path = Path(chroma_db_path or os.getenv('CHROMA_DB_PATH', '../chroma_store'))
        self.collection_name = collection_name
        
        # Create directory if it doesn't exist
        self.chroma_db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.chroma_db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "RAMate training documents for RA assistance"}
        )
        
        print(f"ChromaDB initialized at: {self.chroma_db_path}")
        print(f"Collection: {collection_name}")
    
    def generate_embeddings_openrouter(self, texts: List[str], model: str = "text-embedding-ada-002") -> List[List[float]]:
        """
        Generate embeddings using OpenRouter API.
        
        Args:
            texts: List of texts to embed
            model: Embedding model to use
            
        Returns:
            List of embedding vectors
        """
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            print("OPENROUTER_API_KEY not found, falling back to local embeddings")
            return self.generate_embeddings_local(texts)
        
        embeddings = []
        
        for text in texts:
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/embeddings",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "input": text
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    embedding = result['data'][0]['embedding']
                    embeddings.append(embedding)
                else:
                    print(f"Error getting embedding: {response.status_code} - {response.text}")
                    # Fallback to local embeddings
                    return self.generate_embeddings_local(texts)
                    
            except Exception as e:
                print(f"Error generating embedding for text: {str(e)}")
                # Fallback to local embeddings
                return self.generate_embeddings_local(texts)
        
        return embeddings
    
    def generate_embeddings_local(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using a local sentence transformer model.
        Fallback option if OpenRouter API is not available.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            from sentence_transformers import SentenceTransformer
            
            # Use all-MiniLM-L6-v2 model as specified
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embeddings = model.encode(texts)
            return embeddings.tolist()
            
        except ImportError:
            print("sentence-transformers not available. Install with: pip install sentence-transformers")
            # Return dummy embeddings as fallback
            return [[0.0] * 384 for _ in texts]  # MiniLM embedding size
    
    def add_documents(self, chunks: List[Dict[str, Any]], use_openrouter: bool = True):
        """
        Add document chunks to the vector store.
        
        Args:
            chunks: List of document chunks with metadata
            use_openrouter: Whether to use OpenRouter API for embeddings
        """
        if not chunks:
            print("No chunks to add to vector store")
            return
        
        print(f"Adding {len(chunks)} chunks to vector store...")
        
        # Prepare data for ChromaDB
        texts = [chunk['text'] for chunk in chunks]
        ids = [str(uuid.uuid4()) for _ in chunks]
        
        # Prepare metadata (ChromaDB requires string values)
        metadatas = []
        for chunk in chunks:
            metadata = {
                'source_file': chunk['source_file'],
                'document_title': chunk['document_title'],
                'page_number': str(chunk['page_number']),
                'chunk_index': str(chunk['chunk_index']),
                'document_link': chunk['document_link'],
                'word_count': str(chunk['word_count'])
            }
            metadatas.append(metadata)
        
        # Generate embeddings
        if use_openrouter and os.getenv('OPENROUTER_API_KEY'):
            print("Generating embeddings using OpenRouter API...")
            embeddings = self.generate_embeddings_openrouter(texts)
        else:
            print("Generating embeddings using local model...")
            embeddings = self.generate_embeddings_local(texts)
        
        # Add to ChromaDB
        try:
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ Successfully added {len(chunks)} chunks to vector store")
            
        except Exception as e:
            print(f"❌ Error adding chunks to vector store: {str(e)}")
    
    def search_similar(self, query: str, top_k: int = 5, use_openrouter: bool = True) -> List[Dict[str, Any]]:
        """
        Search for similar documents using vector similarity.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            use_openrouter: Whether to use OpenRouter for query embedding
            
        Returns:
            List of similar documents with metadata
        """
        # Generate embedding for query - always use same method as stored embeddings
        if use_openrouter and os.getenv('OPENROUTER_API_KEY'):
            query_embedding = self.generate_embeddings_openrouter([query])[0]
        else:
            query_embedding = self.generate_embeddings_local([query])[0]
        
        # Search in ChromaDB
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Format results
            formatted_results = []
            
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    result = {
                        'text': doc,
                        'metadata': results['metadatas'][0][i],
                        'similarity_score': 1 - results['distances'][0][i]  # Convert distance to similarity
                    }
                    formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            print(f"Error searching vector store: {str(e)}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store collection.
        
        Returns:
            Dictionary with collection statistics
        """
        try:
            count = self.collection.count()
            
            # Get sample documents to analyze sources
            sample_results = self.collection.peek(limit=min(count, 100))
            
            sources = set()
            if sample_results['metadatas']:
                sources = set(meta.get('source_file', 'Unknown') for meta in sample_results['metadatas'])
            
            return {
                'total_chunks': count,
                'unique_sources': len(sources),
                'source_files': list(sources)
            }
            
        except Exception as e:
            print(f"Error getting collection stats: {str(e)}")
            return {}
    
    def clear_collection(self):
        """Clear all documents from the collection."""
        try:
            # Delete and recreate collection
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "RAMate training documents for RA assistance"}
            )
            print("✅ Collection cleared successfully")
            
        except Exception as e:
            print(f"Error clearing collection: {str(e)}")


def main():
    """Main function to test embedding and vector store functionality."""
    
    from parse_pdfs import PDFProcessor
    
    # Load configuration
    pdf_dir = os.getenv('PDF_DIRECTORY', '../pdfs')
    chroma_path = os.getenv('CHROMA_DB_PATH', '../chroma_store')
    
    # Initialize managers
    pdf_processor = PDFProcessor(pdf_directory=pdf_dir)
    embedding_manager = EmbeddingManager(chroma_db_path=chroma_path)
    
    try:
        # Check if we should clear existing data
        stats = embedding_manager.get_collection_stats()
        if stats.get('total_chunks', 0) > 0:
            print(f"Found existing data: {stats}")
            response = input("Clear existing data? (y/N): ").strip().lower()
            if response == 'y':
                embedding_manager.clear_collection()
        
        # Process PDFs and add to vector store
        print("Processing PDFs...")
        chunks = pdf_processor.process_all_pdfs()
        
        if chunks:
            print("Adding documents to vector store...")
            embedding_manager.add_documents(chunks, use_openrouter=False)  # Use local embeddings for testing
            
            # Test search
            print("\n🔍 Testing search functionality...")
            test_queries = [
                "emergency evacuation procedures",
                "prohibited items in residence halls",
                "duty protocols for paraprofessionals"
            ]
            
            for query in test_queries:
                print(f"\nQuery: '{query}'")
                results = embedding_manager.search_similar(query, top_k=3, use_openrouter=False)
                
                for i, result in enumerate(results, 1):
                    print(f"  {i}. {result['metadata']['document_title']} (Page {result['metadata']['page_number']})")
                    print(f"     Similarity: {result['similarity_score']:.3f}")
                    print(f"     Text: {result['text'][:200]}...")
            
            # Print final stats
            final_stats = embedding_manager.get_collection_stats()
            print(f"\n📊 Final Statistics:")
            print(f"Total chunks in vector store: {final_stats['total_chunks']}")
            print(f"Source documents: {final_stats['unique_sources']}")
            
        else:
            print("No chunks were processed")
            
    except Exception as e:
        print(f"Error in main execution: {str(e)}")


if __name__ == "__main__":
    main()
