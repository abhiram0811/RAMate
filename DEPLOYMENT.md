# RAMate Deployment Guide

🚀 **Complete guide for deploying RAMate to various hosting platforms**

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Local Production Testing](#local-production-testing)
3. [Platform-Specific Guides](#platform-specific-guides)
4. [Environment Configuration](#environment-configuration)
5. [Security Considerations](#security-considerations)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)

## ✅ Pre-Deployment Checklist

### Backend Preparation
- [ ] OpenRouter API key configured in environment
- [ ] PDF documents uploaded to deployment environment
- [ ] Vector store initialized with `python setup.py`
- [ ] API endpoints tested with `python test_api.py`
- [ ] Dependencies pinned in `requirements.txt`

### Frontend Preparation
- [ ] Backend API URL configured in `.env.local`
- [ ] Production build tested with `npm run build`
- [ ] All environment variables set for production
- [ ] Error handling verified for API failures

### Security
- [ ] No API keys in source code
- [ ] CORS origins configured for production domain
- [ ] Rate limiting implemented (if needed)
- [ ] HTTPS enabled for production

## 🧪 Local Production Testing

### Backend Production Mode
```bash
cd backend

# Install production dependencies
pip install gunicorn

# Test production server
gunicorn --bind 0.0.0.0:5000 app:app

# Test with SSL (if certificate available)
gunicorn --bind 0.0.0.0:5000 --certfile cert.pem --keyfile key.pem app:app
```

### Frontend Production Build
```bash
cd frontend

# Create production build
npm run build

# Test production build locally
npm run start
```

## 🌐 Platform-Specific Guides

### 1. Heroku Deployment

#### Backend (Python App)
```bash
# Create Procfile
echo "web: gunicorn app:app" > backend/Procfile

# Create runtime.txt
echo "python-3.13.0" > backend/runtime.txt

# Deploy to Heroku
cd backend
heroku create ramate-backend
heroku config:set OPENROUTER_API_KEY=your_key_here
git subtree push --prefix backend heroku master
```

#### Frontend (Next.js App)
```bash
# Deploy frontend to Vercel (recommended for Next.js)
cd frontend
npm install -g vercel
vercel --prod
```

### 2. AWS Deployment

#### Backend (EC2 + Elastic Beanstalk)
```bash
# Install EB CLI
pip install awsebcli

# Initialize and deploy
cd backend
eb init
eb create ramate-production
eb setenv OPENROUTER_API_KEY=your_key_here
eb deploy
```

#### Frontend (S3 + CloudFront)
```bash
# Build and deploy to S3
npm run build
aws s3 sync ./out s3://your-bucket-name
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"
```

### 3. Google Cloud Platform

#### Backend (Cloud Run)
```dockerfile
# Create Dockerfile in backend/
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
```

```bash
# Deploy to Cloud Run
cd backend
gcloud run deploy ramate-backend --source .
```

#### Frontend (Firebase Hosting)
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Initialize and deploy
cd frontend
npm run build
firebase init hosting
firebase deploy
```

### 4. DigitalOcean App Platform

#### Backend Configuration (`app.yaml`):
```yaml
name: ramate
services:
- name: backend
  source_dir: backend
  github:
    repo: your-username/RAMate
    branch: main
  run_command: gunicorn --worker-tmp-dir /dev/shm app:app
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: OPENROUTER_API_KEY
    scope: RUN_TIME
    value: your_key_here

- name: frontend
  source_dir: frontend
  github:
    repo: your-username/RAMate
    branch: main
  build_command: npm run build
  run_command: npm start
  environment_slug: node-js
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: NEXT_PUBLIC_API_URL
    scope: RUN_AND_BUILD_TIME
    value: ${backend.PUBLIC_URL}
```

### 5. Railway Deployment

#### Simple One-Click Deploy
```bash
# Backend
cd backend
railway login
railway init
railway add
railway deploy

# Frontend  
cd frontend
railway init
railway add
railway deploy
```

## ⚙️ Environment Configuration

### Production Environment Variables

#### Backend (`.env`):
```bash
# Required
OPENROUTER_API_KEY=your_production_api_key

# Production settings
FLASK_ENV=production
FLASK_DEBUG=False
CORS_ORIGINS=https://your-frontend-domain.com

# Database
CHROMA_PERSIST_DIRECTORY=/app/chroma_store

# Performance
MAX_TOKENS=800
REQUEST_TIMEOUT=30
```

#### Frontend (`.env.local`):
```bash
# Production API URL
NEXT_PUBLIC_API_URL=https://your-backend-domain.com

# Analytics (optional)
NEXT_PUBLIC_ANALYTICS_ID=your_analytics_id
```

### Docker Deployment

#### Backend Dockerfile:
```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create volume for persistent storage
VOLUME ["/app/chroma_store"]

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

#### Frontend Dockerfile:
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Expose port
EXPOSE 3000

# Start application
CMD ["npm", "start"]
```

#### Docker Compose:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - CORS_ORIGINS=http://localhost:3000
    volumes:
      - chroma_data:/app/chroma_store
      - ./pdfs:/app/pdfs:ro

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:5000
    depends_on:
      - backend

volumes:
  chroma_data:
```

## 🔒 Security Considerations

### API Security
- Use HTTPS in production
- Implement rate limiting
- Validate all inputs
- Use environment variables for secrets
- Enable CORS only for trusted domains

### Database Security
- Backup vector store regularly
- Use read-only access for PDF files
- Monitor disk usage
- Implement access logging

### Network Security
- Use reverse proxy (nginx/CloudFlare)
- Enable DDoS protection
- Monitor unusual traffic patterns
- Implement IP whitelisting if needed

## 📊 Monitoring and Maintenance

### Health Monitoring
```bash
# Set up monitoring endpoints
GET /api/status      # System health
GET /api/metrics     # Performance metrics
```

### Logging
```python
# Production logging configuration
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Backup Strategy
```bash
# Backup vector store
tar -czf chroma_backup_$(date +%Y%m%d).tar.gz chroma_store/

# Backup configuration
cp .env .env.backup.$(date +%Y%m%d)
```

### Performance Optimization
- Monitor response times
- Scale horizontally if needed
- Optimize database queries
- Use CDN for static assets
- Enable gzip compression

## 🚀 Quick Deploy Commands

### Vercel (Frontend) + Railway (Backend)
```bash
# Deploy backend to Railway
cd backend
railway login
railway init
railway up

# Deploy frontend to Vercel
cd frontend
vercel --prod
```

### Netlify (Frontend) + Render (Backend)
```bash
# Deploy backend to Render
cd backend
# Push to GitHub, connect on Render dashboard

# Deploy frontend to Netlify
cd frontend
npm run build
netlify deploy --prod --dir=out
```

This deployment guide covers all major platforms and scenarios for your RAMate experiments. Choose the platform that best fits your needs and budget! 🚀
