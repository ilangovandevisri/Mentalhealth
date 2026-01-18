# Mental Health Risk Detection System - Quick Start Guide

## 📋 Requirements
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Docker & Docker Compose (optional, for containerized deployment)

---

## 🚀 Quick Start (Development)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure .env
cp .env.example .env

# Run database initialization (if using local PostgreSQL)
cd ../database
python init_db.py

# Start backend server
cd ../backend
python main.py
```

**Backend URL**: http://localhost:8000
**API Docs**: http://localhost:8000/docs

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

**Frontend URL**: http://localhost:3000

---

## 🐳 Quick Start with Docker

### 1. Using Docker Compose (Recommended)

```bash
# Navigate to project root
cd risk

# Start all services
docker-compose up -d

# Initialize database
docker-compose exec backend python database/init_db.py
```

**Access Applications**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database: localhost:5432

### 2. Stop Services

```bash
docker-compose down
```

### 3. View Logs

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

---

## 🤖 Train ML Models

```bash
cd ml

# Train machine learning models
python train_model.py

# This will:
# - Generate synthetic training data (if not available)
# - Train Random Forest model
# - Train Gradient Boosting model
# - Save models to ml/models/trained_models/
```

---

## 📊 Testing the System

### 1. Access Frontend
Open http://localhost:3000 in your browser

### 2. Complete User Flow

```
1. Register account
   - Email, username, password
   - Personal info (name, age, gender)

2. Select assessment
   - PHQ-9 (Depression screening)
   - GAD-7 (Anxiety screening)

3. Complete questionnaire
   - Answer all questions with appropriate ratings

4. View results
   - Risk level (Low/Medium/High/Critical)
   - Risk score (0-100)
   - Contributing factors
   - Personalized recommendations
```

### 3. API Testing with cURL

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPass123",
    "full_name": "Test User",
    "age": 30,
    "gender": "male"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123"
  }'

# Get questionnaires
curl -X GET http://localhost:8000/api/v1/assessment/questionnaires
```

---

## 📁 Project Structure

```
risk/
├── backend/              # FastAPI backend
├── frontend/             # React frontend
├── ml/                   # Machine learning models
│   ├── train_model.py   # ML training script
│   └── rag/             # RAG implementation
├── database/            # Database files
├── docs/                # Documentation
├── docker-compose.yml   # Docker orchestration
└── README.md            # Main documentation
```

---

## 🔑 Default Credentials

**Database** (if using docker-compose):
- Username: `health_user`
- Password: `secure_password`
- Database: `mental_health_db`

---

## 🛠️ Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
netstat -an | grep 8000

# Kill process using port 8000
kill -9 <PID>
```

### Database connection error
```bash
# Check database is running
psql -U health_user -d mental_health_db -h localhost

# Verify DATABASE_URL in .env
```

### Frontend not loading
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Docker issues
```bash
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check logs
docker-compose logs -f
```

---

## 📚 Documentation

- **[Main README](./docs/README.md)** - Complete project overview
- **[API Documentation](./docs/API_DOCUMENTATION.md)** - Full API reference
- **[ML Models](./docs/ML_MODELS.md)** - ML/AI implementation details
- **[Deployment Guide](./docs/DEPLOYMENT.md)** - Production deployment

---

## 🚀 Deployment

### Using Docker to Production

```bash
# Build images for production
docker build -t mental-health-backend:1.0 ./backend
docker build -t mental-health-frontend:1.0 ./frontend

# Push to registry
docker tag mental-health-backend:1.0 your-registry/mental-health-backend:1.0
docker push your-registry/mental-health-backend:1.0

# Deploy using docker-compose or Kubernetes
```

See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for detailed instructions.

---

## ✅ Feature Checklist

- ✅ User Authentication (Register, Login, JWT)
- ✅ Multiple Questionnaires (PHQ-9, GAD-7)
- ✅ Risk Assessment & Scoring
- ✅ Machine Learning Prediction (RF, GB)
- ✅ Deep Learning Models (DL, Attention)
- ✅ RAG System for Resources
- ✅ Risk Visualization Dashboard
- ✅ Personalized Recommendations
- ✅ Audit Logging
- ✅ RESTful API
- ✅ Responsive Frontend UI
- ✅ Docker Support
- ✅ Database Integration (PostgreSQL)
- ✅ Comprehensive Documentation

---

## 📞 Support

For issues or questions:
- Check documentation in `/docs` folder
- Review API documentation at `/api/v1/docs`
- Check logs: `docker-compose logs`

---

**Version**: 1.0.0
**Last Updated**: January 2026
