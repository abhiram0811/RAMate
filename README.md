# RAMate - RA Assistant System

🎓 **A Retrieval-Augmented Generation (RAG) syste## 📸 Demo Screenshots

### Main Chat Interface
![RAMate Chat Interface](https://github.com/user-attachments/assets/b01c32d5-034b-46d3-a799-15372e8fe6df)
*The main chat interface showing a conversation about emergency evacuation procedures*

### Response with Citations
![Response with Sources](https://github.com/user-attachments/assets/0753a7a1-823e-4a62-b55a-18dc602183cd)
*Example response showing proper source citations and confidence scoring*




![RAMate Demo](https://img.shields.io/badge/Status-Operational-brightgreen)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![React](https://img.shields.io/badge/React-18-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)

## 🌟 Features

- **📄 PDF Processing**: Automatically processes RA training documents
- **🧠 Smart Search**: Uses AI embeddings to find relevant information
- **💬 Chat Interface**: Natural language Q&A with training documents
- **📚 Source Citations**: Every answer includes proper citations and page numbers
- **🔗 Document Links**: Direct links to original PDF sources
- **👍 Feedback System**: Users can rate response quality
- **⚡ Real-time**: Fast responses with confidence scoring
- **🎨 Modern UI**: Clean, responsive interface built with Next.js

## 🏗️ System Architecture

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│                 │ ◄──────────────► │                 │
│   Frontend      │                 │    Backend      │
│   (Next.js)     │                 │    (Flask)      │
│   Port: 3000    │                 │   Port: 5000    │
└─────────────────┘                 └─────────────────┘
                                               │
                                               ▼
                                    ┌─────────────────┐
                                    │   ChromaDB      │
                                    │ (Vector Store)  │
                                    └─────────────────┘
                                               │
                                               ▼
                                    ┌─────────────────┐
                                    │  PDF Training   │
                                    │   Documents     │
                                    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+
- npm or yarn

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/ramate.git
cd ramate
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your OpenRouter API key

# Initialize the system
python setup.py

# Start backend server
python app.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## � Demo Screenshots

### Main Chat Interface
![RAMate Chat Interface](docs/images/chat-interface.png)
*The main chat interface showing a conversation about emergency evacuation procedures*

### System Status Dashboard
![System Status](docs/images/system-status.png)
*Real-time system status showing document count and API health*

### Response with Citations
![Response with Sources](docs/images/response-citations.png)
*Example response showing proper source citations and confidence scoring*

### Mobile Responsive Design
![Mobile Interface](docs/images/mobile-interface.png)
*RAMate works seamlessly on mobile devices*

## �📁 Project Structure

```
ramate/
├── backend/                 # Python Flask API
│   ├── app.py              # Main Flask application
│   ├── setup.py            # System initialization
│   ├── parse_pdfs.py       # PDF processing
│   ├── embed_and_store.py  # Embedding & vector storage
│   ├── rag_engine.py       # RAG pipeline
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment configuration
│   └── logs/              # Application logs
├── frontend/               # Next.js React application
│   ├── src/
│   │   ├── app/           # Next.js 14 app directory
│   │   ├── components/    # React components
│   │   └── lib/          # Utilities and API client
│   ├── package.json       # Node.js dependencies
│   └── tailwind.config.js # Styling configuration
├── chroma_store/          # Vector database storage
├── pdfs/                  # Training document storage
└── README.md             # This file
```

## 🔧 Configuration

### Backend Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENROUTER_API_KEY` | OpenRouter API key for AI responses | Yes |
| `NGROK_AUTH_TOKEN` | Ngrok token for public tunneling | Optional |
| `FLASK_PORT` | Backend server port | No (default: 5000) |
| `CHROMA_DB_PATH` | Vector database storage path | No |
| `PDF_DIRECTORY` | Training documents location | No |
| `TOP_K_RESULTS` | Number of results to retrieve | No (default: 3) |

### Frontend Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | Yes |

## 📊 Current Performance

- **Documents Processed**: 5 PDF training manuals
- **Text Chunks**: 119 searchable segments
- **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Response Time**: ~2-5 seconds average
- **Vector Store**: ChromaDB with persistent storage

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.0
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **PDF Processing**: PyPDF2
- **AI Provider**: OpenRouter (DeepSeek model)

### Frontend
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Native fetch API

## 📝 API Documentation

### Backend Endpoints

#### Health Check
```http
GET /
```

#### System Status
```http
GET /api/status
```

#### Chat (Main RAG)
```http
POST /api/chat
Content-Type: application/json

{
  "query": "What are emergency procedures?",
  "session_id": "optional-session-id"
}
```

#### User Feedback
```http
POST /api/feedback
Content-Type: application/json

{
  "query": "original query",
  "answer": "system response",
  "rating": "thumbs_up",
  "comment": "optional comment"
}
```

#### Rebuild Index (Admin)
```http
POST /api/rebuild
Authorization: Bearer admin123
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python test_api.py
```

### Manual Testing
1. Visit http://localhost:3000
2. Ask a question about RA procedures
3. Verify response includes citations and sources
4. Test feedback system with thumbs up/down

## 📈 Monitoring & Logging

- **Interaction Logs**: `backend/logs/interactions_YYYYMMDD.jsonl`
- **Feedback Logs**: `backend/logs/feedback_YYYYMMDD.jsonl`
- **System Status**: Available at `/api/status`
- **Health Monitoring**: Built-in health checks

## 🚀 Deployment

### Development
- Backend: `python app.py`
- Frontend: `npm run dev`

### Production
1. **Backend**: Use production WSGI server (gunicorn, uWSGI)
2. **Frontend**: Deploy to Vercel, Netlify, or similar
3. **Database**: Consider hosted ChromaDB or alternatives
4. **Monitoring**: Set up error tracking and analytics

## 🔮 Future Enhancements

- [ ] Multi-user authentication
- [ ] Document upload interface
- [ ] Advanced search filters
- [ ] Response caching
- [ ] Mobile-optimized interface
- [ ] Integration with campus systems
- [ ] Analytics dashboard
- [ ] Multi-language support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Colorado State University Housing & Dining Services
- OpenRouter for AI model access
- ChromaDB for vector storage
- The open-source community

## 📞 Support

For questions or issues:
- Create an issue on GitHub
- Contact the development team
- Check the documentation in `/backend/README.md` and `/frontend/README.md`

---

**RAMate v1.0** - Helping RAs help residents, one question at a time. 🏠✨
