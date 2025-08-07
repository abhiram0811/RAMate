"""
Flask API Backend for RAMate - RA Assistant System.
Provides REST endpoints for chat functionality and system management.
"""

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from rag_engine import RAGEngine
from embed_and_store import EmbeddingManager
from parse_pdfs import PDFProcessor

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize RAG engine
chroma_path = os.getenv('CHROMA_DB_PATH', '../chroma_store')
rag_engine = RAGEngine(chroma_db_path=chroma_path)

# Request logging for development
@app.before_request
def log_request():
    """Log incoming requests for debugging."""
    if app.debug:
        print(f"[{datetime.now()}] {request.method} {request.path}")
        if request.is_json:
            print(f"Request body: {request.get_json()}")

@app.after_request
def after_request(response):
    """Add CORS headers and log response."""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# API Routes

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'RAMate API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/status', methods=['GET'])
def system_status():
    """Get system status and configuration."""
    try:
        status = rag_engine.get_system_status()
        
        return jsonify({
            'status': 'success',
            'data': status,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error getting system status: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint for RAG queries.
    
    Expected JSON body:
    {
        "query": "What are the emergency procedures?",
        "session_id": "optional-session-id"
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'status': 'error',
                'message': 'Request must be JSON'
            }), 400
        
        data = request.get_json()
        query = data.get('query', '').strip()
        session_id = data.get('session_id', 'anonymous')
        
        if not query:
            return jsonify({
                'status': 'error',
                'message': 'Query is required'
            }), 400
        
        if len(query) > 1000:
            return jsonify({
                'status': 'error',
                'message': 'Query too long (max 1000 characters)'
            }), 400
        
        # Process query with RAG engine
        result = rag_engine.answer_question(query)
        
        # Log the interaction (for development/improvement)
        log_interaction(query, result, session_id)
        
        # Return response
        return jsonify({
            'status': 'success',
            'data': {
                'answer': result['answer'],
                'sources': result['sources'],
                'links': result['links'],
                'confidence': result['confidence'],
                'query': query,
                'timestamp': datetime.now().isoformat()
            }
        })
    
    except Exception as e:
        print(f"Error processing chat request: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error. Please try again.',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/feedback', methods=['POST'])
def feedback():
    """
    Endpoint for user feedback on responses.
    
    Expected JSON body:
    {
        "query": "original query",
        "answer": "system answer",
        "rating": "thumbs_up" | "thumbs_down",
        "comment": "optional comment"
    }
    """
    try:
        if not request.is_json:
            return jsonify({
                'status': 'error',
                'message': 'Request must be JSON'
            }), 400
        
        data = request.get_json()
        
        # Log feedback
        feedback_data = {
            'query': data.get('query', ''),
            'answer': data.get('answer', ''),
            'rating': data.get('rating', ''),
            'comment': data.get('comment', ''),
            'timestamp': datetime.now().isoformat()
        }
        
        log_feedback(feedback_data)
        
        return jsonify({
            'status': 'success',
            'message': 'Feedback received. Thank you!',
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Error processing feedback: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Error saving feedback',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/rebuild', methods=['POST'])
def rebuild_index():
    """
    Rebuild the vector store index from PDFs.
    This is an admin endpoint for updating the knowledge base.
    """
    try:
        # Check if this is authorized (in production, add proper auth)
        auth_token = request.headers.get('Authorization')
        if auth_token != f"Bearer {os.getenv('ADMIN_TOKEN', 'admin123')}":
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized'
            }), 401
        
        # Initialize components
        pdf_dir = os.getenv('PDF_DIRECTORY', '../pdfs')
        pdf_processor = PDFProcessor(pdf_directory=pdf_dir)
        embedding_manager = EmbeddingManager(chroma_db_path=chroma_path)
        
        # Clear existing data
        embedding_manager.clear_collection()
        
        # Process PDFs
        chunks = pdf_processor.process_all_pdfs()
        
        if not chunks:
            return jsonify({
                'status': 'error',
                'message': 'No documents found to process'
            }), 400
        
        # Add to vector store
        embedding_manager.add_documents(chunks, use_openrouter=False)
        
        # Get updated stats
        stats = embedding_manager.get_collection_stats()
        
        return jsonify({
            'status': 'success',
            'message': 'Index rebuilt successfully',
            'data': {
                'chunks_processed': len(chunks),
                'total_chunks': stats['total_chunks'],
                'source_files': stats['source_files']
            },
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Error rebuilding index: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error rebuilding index: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

# Error handlers

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'timestamp': datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'timestamp': datetime.now().isoformat()
    }), 500

# Utility functions

def log_feedback(feedback_data: dict):
    """Log user feedback for system improvement."""
    try:
        from pathlib import Path
        
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # Append to feedback log file
        log_file = log_dir / f"feedback_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback_data) + '\n')
    
    except Exception as e:
        print(f"Error logging feedback: {str(e)}")

def log_interaction(query: str, result: dict, session_id: str):
    """Log user interactions for analysis and improvement."""
    try:
        from pathlib import Path
        
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'query': query,
            'answer': result['answer'],
            'sources': result['sources'],
            'confidence': result['confidence'],
            'retrieved_docs_count': result['retrieved_docs_count']
        }
        
        # Append to daily log file
        log_file = log_dir / f"interactions_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    except Exception as e:
        print(f"Error logging interaction: {str(e)}")

def initialize_system():
    """Initialize the system on startup."""
    print("🚀 Initializing RAMate API...")
    
    # Check system status
    status = rag_engine.get_system_status()
    print(f"Vector store status: {status['vector_store_status']}")
    print(f"Total documents: {status['total_documents']}")
    print(f"OpenRouter configured: {status['openrouter_configured']}")
    
    if status['vector_store_status'] == 'empty':
        print("⚠️  Warning: Vector store is empty. Run embed_and_store.py to process documents.")
    
    print("✅ RAMate API initialized successfully!")

if __name__ == '__main__':
    # Initialize system
    initialize_system()
    
    # Get configuration
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print(f"\n🌐 Starting RAMate API on port {port}")
    print(f"Debug mode: {debug}")
    print(f"CORS enabled for frontend communication")
    
    if debug:
        print("\n📋 Available endpoints:")
        print("  GET  /              - Health check")
        print("  GET  /api/status    - System status")
        print("  POST /api/chat      - Main chat endpoint")
        print("  POST /api/feedback  - User feedback")
        print("  POST /api/rebuild   - Rebuild index (admin)")
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
