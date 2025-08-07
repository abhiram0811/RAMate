"""
RAG (Retrieval-Augmented Generation) module for RAMate.
Handles query processing, document retrieval, and response generation.
"""

import os
import json
from typing import List, Dict, Any, Optional
import requests
from dotenv import load_dotenv
from embed_and_store import EmbeddingManager

load_dotenv()

class RAGEngine:
    """Handles the complete RAG pipeline for RAMate."""
    
    def __init__(self, chroma_db_path: str = None):
        """
        Initialize RAG engine.
        
        Args:
            chroma_db_path: Path to ChromaDB storage
        """
        self.embedding_manager = EmbeddingManager(chroma_db_path)
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        self.top_k = int(os.getenv('TOP_K_RESULTS', 5))
        
    def retrieve_relevant_docs(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a given query.
        
        Args:
            query: User query
            top_k: Number of documents to retrieve
            
        Returns:
            List of relevant documents with metadata
        """
        k = top_k or min(3, self.top_k)  # Use top 3 for more focused responses
        
        # Always use local embeddings for consistency
        results = self.embedding_manager.search_similar(
            query=query,
            top_k=k,
            use_openrouter=False  # Use local embeddings for both storage and retrieval
        )
        
        return results
    
    def format_context(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        """
        Format retrieved documents into context for the LLM.
        
        Args:
            retrieved_docs: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        if not retrieved_docs:
            return "No relevant documents found."
        
        context_parts = []
        
        for i, doc in enumerate(retrieved_docs, 1):
            metadata = doc['metadata']
            
            # Create concise context without redundant information
            context_part = f"""[Source {i}]
Document: {metadata['document_title']}
Page: {metadata['page_number']}
Content: {doc['text'].strip()}"""
            context_parts.append(context_part)
        
        return "\n\n".join(context_parts)
    
    def generate_response(self, query: str, context: str) -> str:
        """
        Generate response using OpenRouter API.
        
        Args:
            query: User query
            context: Retrieved document context
            
        Returns:
            Generated response
        """
        if not self.openrouter_api_key:
            return self._generate_fallback_response(query, context)
        
        prompt = self._create_prompt(query, context)
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek/deepseek-chat-v3-0324:free",  # Free DeepSeek model
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are RAMate, a helpful AI assistant for Resident Assistants (RAs) at Colorado State University. You help RAs find information from their training documents."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.3
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"OpenRouter API error: {response.status_code} - {response.text}")
                return self._generate_fallback_response(query, context)
                
        except Exception as e:
            print(f"Error calling OpenRouter API: {str(e)}")
            return self._generate_fallback_response(query, context)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """
        Create a prompt for the LLM with retrieved context.
        
        Args:
            query: User query
            context: Retrieved document context
            
        Returns:
            Formatted prompt
        """
        prompt = f"""You are RAMate, a helpful AI assistant for Resident Assistants (RAs) at Colorado State University. Your job is to provide clear, concise, and practical answers to help RAs do their job effectively.

INSTRUCTIONS:
- Give a direct, actionable answer in 2-3 paragraphs maximum
- Focus on the most important and practical information
- Use bullet points for procedures or lists when helpful
- Always cite your sources at the end using format: (Source: Document Name, Page X)
- Be conversational but professional
- If the context doesn't fully answer the question, say what you know and suggest they contact their supervisor for additional details

CONTEXT FROM RA TRAINING DOCUMENTS:
{context}

QUESTION: {query}

ANSWER (Be concise and practical):"""
        
        return prompt
    
    def _generate_fallback_response(self, query: str, context: str) -> str:
        """
        Generate a fallback response when API is not available.
        
        Args:
            query: User query
            context: Retrieved document context
            
        Returns:
            Fallback response
        """
        if not context or context == "No relevant documents found.":
            return """I apologize, but I couldn't find relevant information in the training documents to answer your question. 

Please try rephrasing your question or contact your supervisor for assistance.

**RAMate** - *Your RA Assistant*"""
        
        # Extract key information from context for a structured response
        sources = []
        content_summaries = []
        
        # Parse the context to extract structured information
        sections = context.split('[Source ')
        for section in sections[1:]:  # Skip empty first section
            lines = section.strip().split('\n')
            if len(lines) >= 3:
                doc_info = lines[1].replace('Document: ', '').strip()
                page_info = lines[2].replace('Page: ', '').strip()
                content = '\n'.join(lines[3:]).replace('Content: ', '').strip()
                
                sources.append(f"{doc_info} (Page {page_info})")
                # Take first 200 characters of content for summary
                content_summaries.append(content[:200] + '...' if len(content) > 200 else content)
        
        # Create a structured response
        response = f"""**Regarding: {query}**

Based on the RA training documents, here's what I found:

"""
        
        # Combine content summaries into a coherent response
        for i, summary in enumerate(content_summaries):
            response += f"• {summary}\n\n"
        
        response += "**Sources:**\n"
        for i, source in enumerate(sources, 1):
            response += f"{i}. {source}\n"
        
        response += "\n*Note: For enhanced AI responses, configure your OpenRouter API key in the system settings.*"
        
        return response
    
    def answer_question(self, query: str) -> Dict[str, Any]:
        """
        Complete RAG pipeline: retrieve documents and generate answer.
        
        Args:
            query: User question
            
        Returns:
            Dictionary containing answer and metadata
        """
        print(f"Processing query: {query}")
        
        # Step 1: Retrieve relevant documents
        retrieved_docs = self.retrieve_relevant_docs(query)
        
        if not retrieved_docs:
            return {
                'answer': "I couldn't find relevant information in the training documents for your query. Please try rephrasing your question or contact your supervisor.",
                'sources': [],
                'links': [],
                'confidence': 0.0
            }
        
        # Step 2: Format context
        context = self.format_context(retrieved_docs)
        
        # Step 3: Generate response
        answer = self.generate_response(query, context)
        
        # Step 4: Extract metadata for frontend
        sources = []
        links = []
        
        for doc in retrieved_docs:
            metadata = doc['metadata']
            source_info = f"{metadata['document_title']} (Page {metadata['page_number']})"
            if source_info not in sources:
                sources.append(source_info)
            
            if metadata['document_link'] not in links:
                links.append(metadata['document_link'])
        
        # Calculate confidence based on similarity scores
        avg_similarity = sum(doc['similarity_score'] for doc in retrieved_docs) / len(retrieved_docs)
        
        return {
            'answer': answer,
            'sources': sources,
            'links': links,
            'confidence': avg_similarity,
            'retrieved_docs_count': len(retrieved_docs)
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get system status for health checks.
        
        Returns:
            System status information
        """
        stats = self.embedding_manager.get_collection_stats()
        
        return {
            'vector_store_status': 'healthy' if stats.get('total_chunks', 0) > 0 else 'empty',
            'total_documents': stats.get('total_chunks', 0),
            'source_files': stats.get('source_files', []),
            'openrouter_configured': bool(self.openrouter_api_key),
            'embedding_method': 'openrouter' if self.openrouter_api_key else 'local'
        }


def main():
    """Test the RAG engine functionality."""
    
    # Initialize RAG engine
    chroma_path = os.getenv('CHROMA_DB_PATH', '../chroma_store')
    rag_engine = RAGEngine(chroma_db_path=chroma_path)
    
    # Check system status
    status = rag_engine.get_system_status()
    print("🔧 System Status:")
    print(json.dumps(status, indent=2))
    
    if status['vector_store_status'] == 'empty':
        print("\n❌ Vector store is empty. Please run embed_and_store.py first to process documents.")
        return
    
    # Test queries
    test_queries = [
        "What are the emergency evacuation procedures?",
        "What items are prohibited in residence halls?",
        "What should I do during duty rounds?",
        "How do I handle a noise complaint?",
        "What are the assembly areas for emergencies?"
    ]
    
    print(f"\n🤖 Testing RAG Engine with {len(test_queries)} queries...\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"{'='*60}")
        print(f"Query {i}: {query}")
        print(f"{'='*60}")
        
        result = rag_engine.answer_question(query)
        
        print(f"Answer:\n{result['answer']}\n")
        print(f"Sources: {result['sources']}")
        print(f"Confidence: {result['confidence']:.3f}")
        print(f"Retrieved documents: {result['retrieved_docs_count']}")
        print()


if __name__ == "__main__":
    main()
