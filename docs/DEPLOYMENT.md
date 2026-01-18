# Deployment & Docker Guide

## Docker Setup

### Prerequisites
- Docker 20.10+
- Docker Compose 1.29+

### Quick Start with Docker Compose

1. **Clone or navigate to project root**
```bash
cd risk
```

2. **Build and start services**
```bash
docker-compose up -d
```

This will start:
- PostgreSQL database (port 5432)
- Backend API (port 8000)
- Frontend (port 3000)

3. **Verify services**
```bash
docker-compose ps
```

4. **View logs**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

5. **Stop services**
```bash
docker-compose down
```

---

## Individual Docker Builds

### Backend Dockerfile

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build:
```bash
cd backend
docker build -t mental-health-backend:1.0 .
docker run -p 8000:8000 --env-file .env mental-health-backend:1.0
```

### Frontend Dockerfile

Create `frontend/Dockerfile`:
```dockerfile
FROM node:16-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

Build:
```bash
cd frontend
docker build -t mental-health-frontend:1.0 .
docker run -p 3000:80 mental-health-frontend:1.0
```

---

## Docker Compose Configuration

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:14-alpine
    container_name: mental_health_db
    environment:
      POSTGRES_USER: health_user
      POSTGRES_PASSWORD: secure_password
      POSTGRES_DB: mental_health_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U health_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: mental_health_api
    environment:
      DATABASE_URL: postgresql://health_user:secure_password@db:5432/mental_health_db
      SECRET_KEY: ${SECRET_KEY:-your-secret-key-here}
      CORS_ORIGINS: '["http://localhost:3000", "http://localhost:8000"]'
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: mental_health_ui
    environment:
      REACT_APP_API_URL: http://localhost:8000/api/v1
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ./frontend/src:/app/src

volumes:
  postgres_data:
```

---

## Environment Variables

Create `.env` file in root:
```env
# Database
DATABASE_URL=postgresql://health_user:secure_password@db:5432/mental_health_db

# JWT
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# ML
ML_MODEL_PATH=./ml/models/trained_models
RAG_ENABLED=true
EMBEDDING_MODEL=all-MiniLM-L6-v2

# API
API_TITLE=Mental Health Risk Detection API
API_VERSION=1.0.0
LOG_LEVEL=INFO
```

---

## Production Deployment

### Using Nginx Reverse Proxy

Create `nginx.conf`:
```nginx
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:80;
}

server {
    listen 80;
    server_name mental-health-app.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name mental-health-app.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # API endpoints
    location /api {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
    }
}
```

Production docker-compose.yml:
```yaml
version: '3.8'

services:
  db:
    image: postgres:14-alpine
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: mental_health_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  backend:
    image: mental-health-backend:1.0
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/mental_health_db
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      - db
    restart: unless-stopped

  frontend:
    image: mental-health-frontend:1.0
    environment:
      REACT_APP_API_URL: https://mental-health-app.com/api/v1
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

volumes:
  postgres_data:
```

---

## Scaling with Docker Swarm

Initialize swarm:
```bash
docker swarm init
```

Deploy stack:
```bash
docker stack deploy -c docker-compose.yml mental-health
```

Scale services:
```bash
docker service scale mental-health_backend=3
```

---

## Kubernetes Deployment

### Prerequisites
- kubectl configured
- Kubernetes cluster running

### Build and Push Images
```bash
# Build images
docker build -t your-registry/mental-health-backend:1.0 ./backend
docker build -t your-registry/mental-health-frontend:1.0 ./frontend

# Push to registry
docker push your-registry/mental-health-backend:1.0
docker push your-registry/mental-health-frontend:1.0
```

### Create Kubernetes Manifests

`k8s/namespace.yaml`:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: mental-health
```

`k8s/deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: mental-health
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: your-registry/mental-health-backend:1.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: database-url
```

Deploy:
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
```

---

## Health Checks

### Docker Healthcheck
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Manual Health Check
```bash
curl http://localhost:8000/health
# Response: {"status": "healthy", "service": "mental-health-risk-detection"}
```

---

## Monitoring

### Using Prometheus & Grafana

Add to docker-compose.yml:
```yaml
prometheus:
  image: prom/prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana
  ports:
    - "3001:3000"
  environment:
    GF_SECURITY_ADMIN_PASSWORD: admin
```

---

## Troubleshooting

### View Logs
```bash
docker-compose logs -f service_name
```

### Access Container Shell
```bash
docker-compose exec backend bash
docker-compose exec db psql -U health_user -d mental_health_db
```

### Database Connection Issues
```bash
docker-compose exec backend python -c "import psycopg2; psycopg2.connect(os.getenv('DATABASE_URL'))"
```

### Clear Data
```bash
docker-compose down -v  # Remove volumes
```

---

**Last Updated**: January 2026
