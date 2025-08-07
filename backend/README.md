# RAMate Backend Documentation

⚙️ **Complete technical guide to the RAMate backend system - Every feature, every endpoint explained!**

## 📋 Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Core Features](#core-features)
4. [API Endpoints](#api-endpoints)
5. [RAG Pipeline](#rag-pipeline)
6. [Vector Database](#vector-database)
7. [AI Integration](#ai-integration)
8. [Data Processing](#data-processing)
9. [Configuration](#configuration)
10. [Development Guide](#development-guide)

## 🌟 Overview

The RAMate backend is a Python-based Flask API that implements a complete Retrieval-Augmented Generation (RAG) system. It processes PDF training documents, creates vector embeddings, and provides intelligent responses to RA queries with proper citations and confidence scores.

### Key Technologies
- **Python 3.13** with modern async features
- **Flask 3.0** for REST API endpoints
- **ChromaDB** for vector storage and retrieval
- **sentence-transformers** for local embeddings
- **OpenRouter API** for AI inference with DeepSeek model
- **PyPDF2** for document processing

### System Capabilities
- ✅ **PDF Document Processing**: Extract text from training manuals
- ✅ **Vector Embeddings**: Generate semantic representations
- ✅ **Intelligent Retrieval**: Find relevant document chunks
- ✅ **AI-Powered Responses**: Generate accurate, cited answers
- ✅ **Confidence Scoring**: Provide reliability metrics
- ✅ **Session Management**: Track conversation context
- ✅ **Feedback Collection**: Learn from user interactions

## 🏗️ System Architecture

### **High-Level Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask API     │    │   Vector DB     │
│   (Next.js)     │◄──►│   (Python)      │◄──►│   (ChromaDB)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   OpenRouter    │
                       │   API (AI)      │
                       └─────────────────┘
```

### **Component Breakdown**
```
backend/
├── app.py                 # Main Flask application
├── rag_engine.py         # RAG pipeline implementation
├── embed_and_store.py    # Vector embedding manager
├── parse_pdfs.py         # PDF processing utilities
├── setup.py              # System initialization
├── test_api.py           # API testing utilities
├── requirements.txt      # Python dependencies
├── .env                  # Configuration variables
└── chroma_store/         # Vector database storage
```

## 🔧 Core Features

### **1. Document Processing Engine**

#### **PDF Text Extraction**
- **File Support**: Multi-page PDF documents
- **Text Cleaning**: Remove headers, footers, special characters
- **Chunk Creation**: Split into semantic segments (500-800 characters)
- **Metadata Preservation**: Track document source and page numbers

#### **Implementation** (`parse_pdfs.py`):
```python
class PDFProcessor:
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        # PyPDF2 text extraction
        
    def chunk_text(self, text: str, chunk_size: int = 600) -> List[str]:
        # Semantic text chunking
        
    def process_pdf_folder(self, folder_path: str) -> List[Dict]:
        # Batch process all PDFs
```

### **2. Vector Embedding System**

#### **Local Embedding Model**
- **Model**: `all-MiniLM-L6-v2` (384 dimensions)
- **Performance**: Fast, lightweight, highly accurate
- **Offline Capability**: No external API dependencies
- **Consistency**: Same embeddings across runs

#### **Implementation** (`embed_and_store.py`):
```python
class EmbeddingManager:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chroma_client = chromadb.PersistentClient(path="./chroma_store")
        
    def generate_embedding(self, text: str) -> List[float]:
        # Generate semantic embedding
        
    def store_documents(self, documents: List[Dict]) -> None:
        # Store in vector database
        
    def search_similar(self, query: str, k: int = 3) -> List[Dict]:
        # Semantic similarity search
```

### **3. RAG Pipeline**

#### **Retrieval Process**
1. **Query Embedding**: Convert user question to vector
2. **Similarity Search**: Find top-K relevant documents  
3. **Context Ranking**: Score and order results
4. **Context Formatting**: Prepare for AI model

#### **Generation Process**
1. **Prompt Engineering**: Craft instruction with context
2. **AI Inference**: Send to OpenRouter API
3. **Response Parsing**: Extract answer and format
4. **Citation Generation**: Add source references
5. **Confidence Scoring**: Calculate reliability metric

#### **Implementation** (`rag_engine.py`):
```python
class RAGEngine:
    def retrieve_relevant_docs(self, query: str, k: int = 3) -> List[Dict]:
        # Semantic document retrieval
        
    def format_context(self, documents: List[Dict]) -> str:
        # Prepare context for AI model
        
    def generate_response(self, query: str, context: str) -> Dict:
        # AI-powered response generation
        
    def calculate_confidence(self, query: str, response: str, sources: List) -> float:
        # Confidence score calculation
```

### **4. API Layer**

#### **Flask Application Structure**
- **CORS Enabled**: Frontend integration support
- **JSON Responses**: Structured API responses
- **Error Handling**: Graceful failure management
- **Request Logging**: Debug and monitoring support

#### **Endpoint Categories**:
1. **Health Check**: System status monitoring
2. **Chat Interface**: Main RAG functionality
3. **Admin Tools**: System management
4. **Feedback Collection**: User interaction tracking

## 🔌 API Endpoints

### **1. Health Check Endpoint**

#### `GET /api/status`
**Purpose**: Check API health and system status

**Request**: No parameters required
```bash
curl http://localhost:5000/api/status
```

**Response**:
```json
{
  "status": "healthy",
  "message": "RAMate API is running",
  "version": "1.0.0",
  "documents_loaded": 119,
  "vector_store_status": "ready",
  "ai_model": "deepseek/deepseek-chat-v3-0324:free",
  "embedding_model": "all-MiniLM-L6-v2"
}
```

**Status Codes**:
- `200`: API healthy and operational
- `500`: System error or initialization failure

---

### **2. Chat Endpoint**

#### `POST /api/chat`
**Purpose**: Main RAG functionality - answer user questions

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "query": "What should I do during emergency evacuations?",
  "session_id": "session_1754553238959_4in09ljf2"
}
```

**Response**:
```json
{
  "response": "During emergency evacuations, your priority is to ensure resident safety...",
  "sources": [
    {
      "document": "Emergency Evacuation Assembly Areas Synopsis.pdf",
      "page": 1,
      "content": "In case of emergency, RAs must guide residents to designated assembly areas..."
    },
    {
      "document": "FA24 Duty Protocol Snapshot.Parapro.pdf", 
      "page": 3,
      "content": "Emergency procedures require immediate notification of emergency services..."
    }
  ],
  "confidence": 0.87,
  "session_id": "session_1754553238959_4in09ljf2",
  "timestamp": "2024-01-15T14:30:45Z",
  "query_id": "query_1754553245123"
}
```

**Error Responses**:
```json
{
  "error": "Query cannot be empty",
  "status": "error",
  "timestamp": "2024-01-15T14:30:45Z"
}
```

**Status Codes**:
- `200`: Successful response generation
- `400`: Invalid request (missing query/session_id)
- `500`: Internal server error (AI API failure, etc.)

---

### **3. Feedback Endpoint**

#### `POST /api/feedback`
**Purpose**: Collect user feedback on response quality

**Request Body**:
```json
{
  "query_id": "query_1754553245123",
  "session_id": "session_1754553238959_4in09ljf2",
  "rating": "thumbs_up",
  "comment": "Very helpful response with clear instructions",
  "timestamp": "2024-01-15T14:32:10Z"
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Feedback recorded successfully",
  "feedback_id": "feedback_1754553251789"
}
```

**Rating Options**:
- `"thumbs_up"`: Positive feedback
- `"thumbs_down"`: Negative feedback

---

### **4. Admin Endpoints**

#### `GET /api/admin/stats`
**Purpose**: System statistics and monitoring

**Response**:
```json
{
  "total_documents": 5,
  "total_chunks": 119,
  "total_queries": 47,
  "average_confidence": 0.82,
  "vector_store_size": "2.4 MB",
  "uptime": "2 hours 15 minutes",
  "last_updated": "2024-01-15T12:15:30Z"
}
```

#### `POST /api/admin/reload`
**Purpose**: Reload documents and rebuild vector store

**Response**:
```json
{
  "status": "success", 
  "message": "Vector store reloaded successfully",
  "documents_processed": 5,
  "chunks_created": 119,
  "processing_time": "12.3 seconds"
}
```

## 🧠 RAG Pipeline Details

### **1. Query Processing**

#### **Input Validation**
```python
def validate_query(query: str) -> bool:
    if not query or len(query.strip()) == 0:
        return False
    if len(query) > 1000:  # Character limit
        return False
    return True
```

#### **Query Enhancement**
```python
def enhance_query(query: str) -> str:
    # Add context keywords for better retrieval
    enhanced = f"RA training {query} procedures policy"
    return enhanced
```

### **2. Document Retrieval**

#### **Similarity Search**
```python
def search_documents(self, query_embedding: List[float], k: int = 3):
    results = self.collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=['documents', 'metadatas', 'distances']
    )
    return results
```

#### **Context Ranking Algorithm**
1. **Semantic Similarity**: Vector cosine similarity (primary)
2. **Keyword Overlap**: Term frequency matching (secondary) 
3. **Document Diversity**: Avoid redundant sources (tertiary)
4. **Recency Bias**: Prefer newer training materials (quaternary)

### **3. Response Generation**

#### **Prompt Engineering**
The system uses carefully crafted prompts for optimal AI responses:

```python
SYSTEM_PROMPT = """
You are RAMate, an AI assistant for Colorado State University Resident Assistants. 
Your role is to provide accurate, helpful information from RA training materials.

Instructions:
1. Give concise, actionable responses (2-3 paragraphs maximum)
2. Use professional but friendly tone appropriate for RAs
3. Include specific procedures and step-by-step instructions when relevant
4. Reference the source materials accurately
5. If information is unclear or missing, acknowledge limitations

Context Guidelines:
- Focus on practical, immediately actionable information
- Prioritize safety procedures and emergency protocols
- Include relevant policy numbers or section references when available
- Clarify any ambiguous terms or procedures
"""

def create_user_prompt(query: str, context: str) -> str:
    return f"""
Based on the following training materials, please answer this RA question:

Question: {query}

Training Materials:
{context}

Please provide a helpful, accurate response with clear action steps.
"""
```

#### **AI Model Configuration**
```python
API_CONFIG = {
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "max_tokens": 800,
    "temperature": 0.3,  # Low for consistent, factual responses
    "top_p": 0.8,
    "presence_penalty": 0.1,
    "frequency_penalty": 0.1
}
```

### **4. Confidence Scoring**

#### **Multi-Factor Confidence Calculation**
```python
def calculate_confidence(self, query: str, response: str, sources: List[Dict]) -> float:
    # Factor 1: Source relevance (40% weight)
    relevance_score = self._calculate_source_relevance(query, sources)
    
    # Factor 2: Response completeness (30% weight) 
    completeness_score = self._calculate_response_completeness(response)
    
    # Factor 3: Factual consistency (20% weight)
    consistency_score = self._calculate_consistency(response, sources)
    
    # Factor 4: Query complexity match (10% weight)
    complexity_score = self._calculate_complexity_match(query, response)
    
    confidence = (
        relevance_score * 0.4 + 
        completeness_score * 0.3 + 
        consistency_score * 0.2 + 
        complexity_score * 0.1
    )
    
    return round(confidence, 3)
```

## 💾 Vector Database

### **ChromaDB Configuration**

#### **Collection Setup**
```python
self.collection = self.chroma_client.get_or_create_collection(
    name="ramate_documents",
    metadata={"description": "RA training documents"},
    embedding_function=None  # Using custom embeddings
)
```

#### **Document Storage Schema**
```python
document_record = {
    "id": f"doc_{index}_{uuid4()}",
    "embedding": embedding_vector,  # 384-dimensional
    "document": chunk_text,
    "metadata": {
        "source": pdf_filename,
        "page": page_number,
        "chunk_index": chunk_index,
        "processed_date": timestamp,
        "chunk_size": len(chunk_text)
    }
}
```

#### **Search Performance**
- **Index Type**: HNSW (Hierarchical Navigable Small World)
- **Distance Metric**: Cosine similarity
- **Search Speed**: ~10ms for top-3 results
- **Memory Usage**: ~50MB for 119 documents
- **Persistence**: Automatic disk storage

### **Database Management**

#### **Initialization**
```python
def initialize_vector_store():
    # Create ChromaDB client
    # Process all PDFs
    # Generate embeddings
    # Store in collection
    # Verify integrity
```

#### **Health Monitoring**
```python
def check_vector_store_health():
    collection_count = self.collection.count()
    sample_search = self.collection.query(
        query_texts=["test query"],
        n_results=1
    )
    return {
        "status": "healthy" if collection_count > 0 else "empty",
        "document_count": collection_count,
        "search_functional": len(sample_search['documents']) > 0
    }
```

## 🤖 AI Integration

### **OpenRouter API Integration**

#### **Authentication Setup**
```python
OPENROUTER_CONFIG = {
    "api_key": os.getenv('OPENROUTER_API_KEY'),
    "base_url": "https://openrouter.ai/api/v1/chat/completions",
    "headers": {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "RAMate - RA Assistant"
    }
}
```

#### **Request Format**
```python
def call_ai_model(self, messages: List[Dict]) -> str:
    payload = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": messages,
        "max_tokens": 800,
        "temperature": 0.3,
        "stream": False
    }
    
    response = requests.post(
        OPENROUTER_CONFIG["base_url"],
        headers=OPENROUTER_CONFIG["headers"],
        json=payload,
        timeout=30
    )
    
    return response.json()["choices"][0]["message"]["content"]
```

#### **Error Handling**
```python
def handle_ai_errors(self, error: Exception) -> str:
    if isinstance(error, requests.exceptions.Timeout):
        return "AI service timeout - please try again"
    elif isinstance(error, requests.exceptions.ConnectionError):
        return "AI service unavailable - please check connection"
    elif "rate_limit" in str(error):
        return "Rate limit exceeded - please wait before retrying"
    else:
        return f"AI service error: {str(error)}"
```

### **Model Selection Rationale**

#### **DeepSeek Chat v3 Benefits**:
- **Free Tier**: No cost for development/testing
- **High Quality**: GPT-4 level performance
- **Fast Response**: ~2-3 second response times
- **Context Length**: 32K tokens (sufficient for RAG)
- **Instruction Following**: Excellent prompt adherence

## 📊 Data Processing

### **PDF Processing Pipeline**

#### **Stage 1: Text Extraction**
```python
def extract_text_from_pdf(self, pdf_path: str) -> str:
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            # Clean and normalize text
            cleaned_text = self.clean_text(page_text)
            text += f"\n[Page {page_num + 1}]\n{cleaned_text}"
    return text
```

#### **Stage 2: Text Cleaning**
```python
def clean_text(self, text: str) -> str:
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove header/footer patterns
    text = re.sub(r'Page \d+ of \d+', '', text)
    
    # Fix common OCR errors
    text = text.replace('fi', 'fi').replace('fl', 'fl')
    
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    
    return text.strip()
```

#### **Stage 3: Semantic Chunking**
```python
def chunk_text(self, text: str, chunk_size: int = 600, overlap: int = 100) -> List[str]:
    # Split by sentences first
    sentences = self.split_into_sentences(text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    
    # Add final chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
```

### **Document Statistics**

#### **Current Dataset**:
- **Total PDFs**: 5 training documents
- **Total Pages**: ~25 pages
- **Total Chunks**: 119 semantic chunks
- **Average Chunk Size**: 580 characters
- **Total Storage**: 2.4 MB vector database

#### **Processing Metrics**:
- **Extraction Speed**: ~0.5 seconds per PDF
- **Embedding Generation**: ~2 seconds per document
- **Total Processing Time**: ~12 seconds for full dataset
- **Memory Usage**: ~200MB during processing

## ⚙️ Configuration

### **Environment Variables**

#### **Required Settings** (`.env`):
```bash
# AI API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Model Configuration  
AI_MODEL=deepseek/deepseek-chat-v3-0324:free
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Database Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_store
VECTOR_COLLECTION_NAME=ramate_documents

# API Configuration
FLASK_PORT=5000
FLASK_DEBUG=True
CORS_ORIGINS=http://localhost:3000

# Processing Configuration
PDF_DIRECTORY=../pdfs
CHUNK_SIZE=600
CHUNK_OVERLAP=100
MAX_RETRIEVAL_RESULTS=3
```

#### **Optional Settings**:
```bash
# Performance Tuning
MAX_TOKENS=800
TEMPERATURE=0.3
REQUEST_TIMEOUT=30

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=ramate.log

# Rate Limiting
REQUESTS_PER_MINUTE=60
BURST_LIMIT=10
```

### **Model Configuration**

#### **Embedding Model Settings**:
```python
EMBEDDING_CONFIG = {
    "model_name": "all-MiniLM-L6-v2",
    "device": "cpu",  # or "cuda" for GPU
    "normalize_embeddings": True,
    "batch_size": 32,
    "max_seq_length": 512
}
```

#### **AI Model Settings**:
```python
AI_MODEL_CONFIG = {
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "max_tokens": 800,
    "temperature": 0.3,
    "top_p": 0.8,
    "presence_penalty": 0.1,
    "frequency_penalty": 0.1,
    "stop": None
}
```

## 🚀 Development Guide

### **Environment Setup**

#### **1. Python Environment**
```bash
# Create virtual environment
python -m venv ramate_env

# Activate environment (Windows)
ramate_env\Scripts\activate

# Activate environment (macOS/Linux)
source ramate_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### **2. Environment Configuration**
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

#### **3. Initialize System**
```bash
# Run setup script
python setup.py

# Verify installation
python test_api.py
```

### **Development Workflow**

#### **1. Start Development Server**
```bash
# With auto-reload
python app.py

# With debug logging
FLASK_DEBUG=True python app.py

# With specific port
FLASK_PORT=5001 python app.py
```

#### **2. Testing API Endpoints**
```bash
# Test health check
curl http://localhost:5000/api/status

# Test chat endpoint
python test_api.py

# Manual testing
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What are emergency procedures?", "session_id": "test_session"}'
```

#### **3. Monitor System Performance**
```bash
# Check vector store
python -c "from embed_and_store import EmbeddingManager; em = EmbeddingManager(); print(em.get_collection_stats())"

# Check processing speed
python -c "from rag_engine import RAGEngine; engine = RAGEngine(); engine.benchmark_query('test query')"
```

### **Code Structure Guidelines**

#### **Module Organization**:
```
backend/
├── app.py              # Flask routes and API logic
├── rag_engine.py       # Core RAG functionality
├── embed_and_store.py  # Vector operations
├── parse_pdfs.py       # Document processing
└── utils/
    ├── logging.py      # Logging configuration
    ├── validation.py   # Input validation
    └── helpers.py      # Utility functions
```

#### **Coding Standards**:
- **Type Hints**: Use comprehensive type annotations
- **Documentation**: Docstrings for all functions
- **Error Handling**: Comprehensive try-catch blocks
- **Logging**: Structured logging for debugging
- **Testing**: Unit tests for core functions

### **Performance Optimization**

#### **Vector Search Optimization**:
```python
# Batch embedding generation
def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
    return self.model.encode(texts, batch_size=32, show_progress_bar=True)

# Async query processing
async def process_query_async(self, query: str) -> Dict:
    # Concurrent embedding and context retrieval
```

#### **Caching Strategy**:
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_embedding(self, text: str) -> List[float]:
    return self.model.encode([text])[0].tolist()
```

#### **Memory Management**:
```python
import gc

def optimize_memory():
    gc.collect()  # Force garbage collection
    torch.cuda.empty_cache()  # Clear GPU memory if using CUDA
```

This comprehensive backend documentation covers every technical aspect of the RAMate system. Whether you're debugging issues, adding new features, or understanding the architecture, this guide provides complete coverage of the backend implementation! 🚀⚙️
