# Google Cloud Platform Setup Guide

Complete guide for deploying the Crypto Curriculum Platform to Google Cloud Platform.

> **Phase 3 Reminder:** Complete the local development milestones first (see `docs/deployment/local-development.md`). Use this guide when you are ready to promote the working build to Google Cloud.

---

## 📋 Prerequisites

- [ ] Google Cloud account created
- [ ] Billing enabled
- [ ] Google Cloud SDK installed locally (`gcloud`)
- [ ] Docker Desktop installed
- [ ] Git repository access
- [ ] 501(c)(3) documentation (for non-profit credits)

---

## 💰 STEP 1: Apply for Google for Nonprofits

### 1.1 Register for Nonprofit Program

**URL:** https://www.google.com/nonprofits/

**Requirements:**
- Valid 501(c)(3) status (or equivalent)
- Organization mission statement
- Website (can use cryptocurriculum.org once purchased)

**Application Process:**
1. Go to Google for Nonprofits
2. Click "Get Started"
3. Verify nonprofit status via TechSoup
4. Submit application
5. Wait for approval (duration varies)

### 1.2 Activate Benefits

Once approved:
- [ ] **$3,000/year** Google Cloud credits (automatic)
- [ ] **$10,000/month** Google Ads grant (apply separately)
- [ ] **Google Workspace** free or discounted (up to 30 users)
- [ ] **YouTube for Nonprofits** (if creating video content)

**Total Value:** $3,000-10,000+/year

---

## ☁️ STEP 2: Set Up Google Cloud Projects

### 2.1 Create Development Project

```bash
# Login to Google Cloud
gcloud auth login

# Create development project
gcloud projects create crypto-curriculum-dev --name="Crypto Curriculum (Dev)"

# Set as default
gcloud config set project crypto-curriculum-dev

# Enable billing
gcloud beta billing projects link crypto-curriculum-dev --billing-account=BILLING_ACCOUNT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable sql-component.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable storage-api.googleapis.com
gcloud services enable logging.googleapis.com
gcloud services enable monitoring.googleapis.com
```

### 2.2 Create Production Project

```bash
# Create production project
gcloud projects create crypto-curriculum-prod --name="Crypto Curriculum (Production)"

# Set as current
gcloud config set project crypto-curriculum-prod

# Enable billing
gcloud beta billing projects link crypto-curriculum-prod --billing-account=BILLING_ACCOUNT_ID

# Enable same APIs as dev
gcloud services enable run.googleapis.com sql-component.googleapis.com sqladmin.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com storage-api.googleapis.com logging.googleapis.com monitoring.googleapis.com
```

### 2.3 Set Up Billing Alerts

```bash
# Set budget alerts
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="Monthly Budget Alert" \
  --budget-amount=100 \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=75 \
  --threshold-rule=percent=90
```

**Alert thresholds:**
- 50% ($50) - Email notification
- 75% ($75) - Email notification
- 90% ($90) - Email + SMS notification

---

## 🗄️ STEP 3: Set Up Cloud SQL (PostgreSQL)

### 3.1 Create Development Database Instance

```bash
gcloud config set project crypto-curriculum-dev

# Create Cloud SQL instance (development)
gcloud sql instances create crypto-curriculum-dev-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --storage-size=10GB \
  --storage-type=SSD \
  --backup \
  --backup-start-time=03:00 \
  --maintenance-window-day=SUN \
  --maintenance-window-hour=04

# Set root password
gcloud sql users set-password postgres \
  --instance=crypto-curriculum-dev-db \
  --password=STRONG_PASSWORD_HERE

# Create application database
gcloud sql databases create crypto_curriculum_dev \
  --instance=crypto-curriculum-dev-db

# Create app user
gcloud sql users create app_user \
  --instance=crypto-curriculum-dev-db \
  --password=APP_USER_PASSWORD
```

### 3.2 Create Production Database Instance

```bash
gcloud config set project crypto-curriculum-prod

# Create Cloud SQL instance (production - more resources)
gcloud sql instances create crypto-curriculum-prod-db \
  --database-version=POSTGRES_15 \
  --tier=db-n1-standard-1 \
  --region=us-central1 \
  --storage-size=20GB \
  --storage-type=SSD \
  --availability-type=ZONAL \
  --backup \
  --backup-start-time=03:00 \
  --maintenance-window-day=SUN \
  --maintenance-window-hour=04 \
  --enable-bin-log \
  --retained-backups-count=7

# Create database and users (same as dev)
```

### 3.3 Configure Database Access

```bash
# Get connection name
gcloud sql instances describe crypto-curriculum-dev-db \
  --format='value(connectionName)'

# Output example: crypto-curriculum-dev:us-central1:crypto-curriculum-dev-db
# Save this for later use in DATABASE_URL
```

---

## 🔐 STEP 4: Set Up Secret Manager

### 4.1 Create Secrets

```bash
# Backend secrets
echo -n "your-secret-key-min-32-chars" | \
  gcloud secrets create backend-secret-key --data-file=-

echo -n "sk-your-openai-key" | \
  gcloud secrets create openai-api-key --data-file=-

echo -n "sk-ant-your-anthropic-key" | \
  gcloud secrets create anthropic-api-key --data-file=-

# Database URL (will be constructed from Cloud SQL connection)
echo -n "postgresql://app_user:APP_USER_PASSWORD@/crypto_curriculum_dev?host=/cloudsql/CONNECTION_NAME" | \
  gcloud secrets create database-url-dev --data-file=-
```

### 4.2 Grant Access to Cloud Run

```bash
# Allow Cloud Run to access secrets
gcloud secrets add-iam-policy-binding backend-secret-key \
  --member='serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com' \
  --role='roles/secretmanager.secretAccessor'

# Repeat for all secrets
```

---

## 🐳 STEP 5: Containerize Applications

### 5.1 Create Backend Dockerfile

**File:** `app/backend/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Cloud Run will inject $PORT)
EXPOSE 8080

# Run with uvicorn
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
```

### 5.2 Create Frontend Dockerfile

**File:** `app/frontend/Dockerfile`

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build for production
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 8080 (Cloud Run requires 8080)
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
```

### 5.3 Create nginx Configuration

**File:** `app/frontend/nginx.conf`

```nginx
server {
    listen 8080;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Enable gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Cache static assets
    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 5.4 Create .dockerignore Files

**File:** `app/backend/.dockerignore`
```
venv/
__pycache__/
*.pyc
.env
.git/
tests/
```

**File:** `app/frontend/.dockerignore`
```
node_modules/
dist/
.env*
.git/
```

---

## 🚀 STEP 6: Deploy to Cloud Run

### 6.1 Build and Push Backend

```bash
cd app/backend

# Build container
gcloud builds submit --tag gcr.io/crypto-curriculum-dev/backend

# Deploy to Cloud Run
gcloud run deploy crypto-curriculum-backend \
  --image gcr.io/crypto-curriculum-dev/backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --min-instances 0 \
  --max-instances 5 \
  --timeout 60s \
  --set-env-vars ENVIRONMENT=development \
  --set-secrets DATABASE_URL=database-url-dev:latest \
  --set-secrets SECRET_KEY=backend-secret-key:latest \
  --set-secrets OPENAI_API_KEY=openai-api-key:latest \
  --add-cloudsql-instances crypto-curriculum-dev:us-central1:crypto-curriculum-dev-db
```

### 6.2 Build and Push Frontend

```bash
cd app/frontend

# Build container
gcloud builds submit --tag gcr.io/crypto-curriculum-dev/frontend

# Deploy to Cloud Run
gcloud run deploy crypto-curriculum-frontend \
  --image gcr.io/crypto-curriculum-dev/frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 256Mi \
  --min-instances 0 \
  --max-instances 10 \
  --set-env-vars VITE_API_URL=https://BACKEND_URL
```

### 6.3 Get Service URLs

```bash
# Backend URL
gcloud run services describe crypto-curriculum-backend \
  --region us-central1 \
  --format 'value(status.url)'

# Frontend URL
gcloud run services describe crypto-curriculum-frontend \
  --region us-central1 \
  --format 'value(status.url)'
```

---

## 🌐 STEP 7: Configure Custom Domain

### 7.1 Purchase Domain

**Recommended:** Google Domains (integrated with GCP)
- Purchase: cryptocurriculum.org
- Cost: ~$12-15/year

### 7.2 Map Domain to Cloud Run

```bash
# Map custom domain to frontend
gcloud beta run domain-mappings create \
  --service crypto-curriculum-frontend \
  --domain cryptocurriculum.org \
  --region us-central1

# Map subdomain to backend
gcloud beta run domain-mappings create \
  --service crypto-curriculum-backend \
  --domain api.cryptocurriculum.org \
  --region us-central1
```

### 7.3 Configure DNS

In Google Domains (or your DNS provider):

```
Type  | Name | Value
------|------|------
A     | @    | (provided by Cloud Run)
AAAA  | @    | (provided by Cloud Run)
A     | api  | (provided by Cloud Run)
AAAA  | api  | (provided by Cloud Run)
CNAME | www  | cryptocurriculum.org
```

**SSL Certificate:** Automatically provisioned by Cloud Run (Let's Encrypt)

---

## 📧 STEP 8: Set Up Email

### Option 1: SendGrid (Recommended)

```bash
# Sign up at sendgrid.com
# Get API key
# Add to Secret Manager
echo -n "SG.your-api-key" | \
  gcloud secrets create sendgrid-api-key --data-file=-
```

**Configuration in backend:**
```python
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = "noreply@cryptocurriculum.org"
```

### Option 2: Google Workspace

If using Google Workspace for Nonprofits:
- Set up admin@cryptocurriculum.org
- Set up support@cryptocurriculum.org
- Set up noreply@cryptocurriculum.org
- Use SMTP or Gmail API

---

## 📊 STEP 9: Set Up Monitoring

### 9.1 Cloud Logging

```bash
# Logs are automatic with Cloud Run
# View logs:
gcloud logging read "resource.type=cloud_run_revision" --limit 50

# Create log-based alerts
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="High Error Rate" \
  --condition-threshold-value=10 \
  --condition-threshold-duration=60s
```

### 9.2 Cloud Monitoring

**Create Dashboard:**
1. Go to Cloud Console → Monitoring → Dashboards
2. Create dashboard: "Crypto Curriculum Platform"
3. Add charts:
   - Request count (Cloud Run)
   - Response latency
   - Error rate
   - Database connections
   - CPU/Memory usage

### 9.3 Uptime Checks

```bash
# Create uptime check
gcloud monitoring uptime create crypto-curriculum-uptime \
  --resource-type=uptime-url \
  --host=cryptocurriculum.org \
  --path=/ \
  --check-interval=5m
```

### 9.4 Alerts

Set up alerts for:
- [ ] Error rate > 5%
- [ ] Response time > 2 seconds
- [ ] Uptime < 99%
- [ ] Database connections > 80%
- [ ] Cost exceeds budget

---

## 🔐 STEP 10: Security Configuration

### 10.1 Enable Cloud Armor (DDoS Protection)

```bash
# Create security policy
gcloud compute security-policies create crypto-curriculum-policy \
  --description "DDoS protection for Crypto Curriculum"

# Add rate limiting rule
gcloud compute security-policies rules create 1000 \
  --security-policy crypto-curriculum-policy \
  --expression "true" \
  --action "rate-based-ban" \
  --rate-limit-threshold-count 100 \
  --rate-limit-threshold-interval-sec 60
```

### 10.2 Configure IAM Roles

```bash
# Create service account for backend
gcloud iam service-accounts create crypto-curriculum-backend \
  --display-name="Crypto Curriculum Backend Service"

# Grant Cloud SQL access
gcloud projects add-iam-policy-binding crypto-curriculum-dev \
  --member="serviceAccount:crypto-curriculum-backend@crypto-curriculum-dev.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"

# Grant Secret Manager access
gcloud projects add-iam-policy-binding crypto-curriculum-dev \
  --member="serviceAccount:crypto-curriculum-backend@crypto-curriculum-dev.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

---

## 🔄 STEP 11: Set Up CI/CD with GitHub Actions

### 11.1 Create Service Account Key

```bash
# Create key for GitHub Actions
gcloud iam service-accounts keys create github-actions-key.json \
  --iam-account=crypto-curriculum-backend@crypto-curriculum-dev.iam.gserviceaccount.com

# Base64 encode for GitHub secret
cat github-actions-key.json | base64
```

### 11.2 Add GitHub Secrets

Go to GitHub repo → Settings → Secrets → Actions

Add secrets:
- `GCP_PROJECT_ID`: crypto-curriculum-dev
- `GCP_SA_KEY`: (base64 encoded service account key)
- `GCP_REGION`: us-central1

### 11.3 Create Deployment Workflow

**File:** `.github/workflows/deploy-dev.yml`

```yaml
name: Deploy to Development

on:
  push:
    branches: [ development ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Cloud SDK
      uses: google-github-actions/setup-gcloud@v1
      with:
        service_account_key: ${{ secrets.GCP_SA_KEY }}
        project_id: ${{ secrets.GCP_PROJECT_ID }}
    
    - name: Configure Docker
      run: gcloud auth configure-docker
    
    - name: Build Backend
      run: |
        cd app/backend
        gcloud builds submit --tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/backend
    
    - name: Deploy Backend
      run: |
        gcloud run deploy crypto-curriculum-backend \
          --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/backend \
          --platform managed \
          --region ${{ secrets.GCP_REGION }} \
          --allow-unauthenticated
    
    - name: Build Frontend
      run: |
        cd app/frontend
        gcloud builds submit --tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/frontend
    
    - name: Deploy Frontend
      run: |
        gcloud run deploy crypto-curriculum-frontend \
          --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/frontend \
          --platform managed \
          --region ${{ secrets.GCP_REGION }} \
          --allow-unauthenticated
```

---

## 🗃️ STEP 12: Database Migrations

### 12.1 Run Initial Migration

```bash
# From app/backend directory with venv activated

# Connect to Cloud SQL via proxy (for migration)
cloud_sql_proxy -instances=CONNECTION_NAME=tcp:5432 &

# Run migrations
alembic upgrade head

# Seed database
python scripts/seed_database.py
```

### 12.2 Automated Migrations in CI/CD

Add to deployment workflow:
```yaml
- name: Run Database Migrations
  run: |
    cd app/backend
    pip install -r requirements.txt
    alembic upgrade head
```

---

## 📈 STEP 13: Set Up Analytics

### 13.1 Google Analytics 4

1. Create GA4 property at analytics.google.com
2. Get Measurement ID (G-XXXXXXXXXX)
3. Add to frontend environment variables
4. Implement tracking in React app

### 13.2 Cloud Monitoring Dashboard

Create custom dashboard with:
- Request volume (by endpoint)
- Response times (p50, p95, p99)
- Error rates
- Database query performance
- User activity (registrations, logins, completions)

---

## 🧪 STEP 14: Testing the Deployment

### 14.1 Health Checks

```bash
# Test backend health
curl https://api.cryptocurriculum.org/health

# Expected response:
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-11-01T12:00:00Z"
}
```

### 14.2 Load Testing

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test with 100 concurrent users
ab -n 1000 -c 100 https://cryptocurriculum.org/

# Monitor in Cloud Monitoring during test
```

---

## 📝 STEP 15: Documentation

### 15.1 Update Environment Variables

**File:** `docs/templates/backend.env.example`

Add Google Cloud specific variables:
```bash
# Google Cloud
GCP_PROJECT_ID=crypto-curriculum-dev
INSTANCE_CONNECTION_NAME=crypto-curriculum-dev:us-central1:crypto-curriculum-dev-db
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

### 15.2 Create Runbook

Document procedures for:
- Deployment process
- Rollback procedure
- Database backup/restore
- Incident response
- Scaling resources
- Cost optimization

---

## 💵 Cost Optimization

### Auto-Scaling Configuration

**Cloud Run:**
- Min instances: 0 (scale to zero when idle)
- Max instances: Adjust based on usage
- Request timeout: 60s (default)
- Concurrency: 80 (default)

**Cloud SQL:**
- Start with smallest tier
- Enable auto-storage increase
- Set connection timeout
- Use connection pooling

### Monitoring Costs

```bash
# Check current month costs
gcloud billing projects describe crypto-curriculum-dev

# View cost breakdown
# Go to: Console → Billing → Reports
```

---

## 🎯 Production Checklist

Before going live:

### Security
- [ ] All secrets in Secret Manager (not env files)
- [ ] HTTPS enforced (automatic with Cloud Run)
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] SQL injection protection (using ORM)
- [ ] XSS protection (sanitized inputs)
- [ ] CSP headers configured

### Performance
- [ ] Lighthouse score >90
- [ ] Page load time <2 seconds
- [ ] API response time <200ms
- [ ] Database queries optimized
- [ ] CDN enabled (Cloud CDN)
- [ ] Images optimized

### Reliability
- [ ] Database backups automated
- [ ] Restore procedure tested
- [ ] Monitoring alerts configured
- [ ] Health checks enabled
- [ ] Error tracking active
- [ ] Uptime monitoring configured

### Legal
- [ ] Privacy Policy published
- [ ] Terms of Service published
- [ ] Cookie consent (if applicable)
- [ ] FERPA compliance documented

### Content
- [ ] All 17 modules loaded
- [ ] All 170 assessments created
- [ ] All images/diagrams uploaded
- [ ] Sample cohort created
- [ ] Test users created

---

## 🔧 Maintenance

### Daily
- Check error logs
- Monitor uptime
- Review support tickets

### Weekly
- Review cost report
- Deploy bug fixes
- Update content as needed

### Monthly
- Security updates
- Performance optimization
- Analytics review
- Backup verification

### Quarterly
- Major feature releases
- Curriculum updates
- Cost optimization review
- User satisfaction survey

---

## 🆘 Troubleshooting

### Common Issues

**"Service Unavailable"**
- Check Cloud Run logs: `gcloud run services logs read crypto-curriculum-backend`
- Verify database connection
- Check if service is running

**"Database connection failed"**
- Verify Cloud SQL instance is running
- Check connection name is correct
- Verify service account has cloudsql.client role
- Check if database exists

**"High costs"**
- Review Cloud Run min instances (should be 0 for dev)
- Check database tier (can downgrade if over-provisioned)
- Review Cloud Storage usage
- Enable auto-scaling limits

---

## 📞 Support

### Google Cloud Support
- **Free:** Community forums, documentation
- **Standard:** $29/month - 4-hour response time
- **Enhanced:** $500/month - 1-hour response time

### Non-Profit Support
- Special support via Google for Nonprofits
- Educational use case prioritization
- Community resources for nonprofits

---

**Last Updated:** 2025-11-01  
**Next Review:** After first deployment
