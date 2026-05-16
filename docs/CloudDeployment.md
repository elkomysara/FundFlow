# 🚀 **Production Deployment to Google Cloud Run - Complete Guide**

Excellent choice! You have a production-ready FastAPI backend with a cloud database already loaded with 103 grants and 50 companies. Let’s deploy it to Google Cloud Run to make your intelligent matching system accessible worldwide.

---

## **📋 Pre-Deployment Quick Check**

Verify these essentials before we begin:

```bash
# Navigate to your project
cd /d/D1/WTF/ImaraFund

# Check required files exist
ls Dockerfile app/main.py requirements.txt .env

# Verify gcloud CLI is installed and authenticated
gcloud --version
gcloud config get-value project

# Check your Cloud SQL database is accessible
python -c "from app.database import SessionLocal; db = SessionLocal(); print('✅ Database connected'); db.close()"
```

**If any check fails, we’ll address it in the setup phase.**

---

## **🔧 Phase 1: Environment Setup (5 minutes)**

### **1.1 Authenticate and Configure gcloud**

```bash
# Login to Google Cloud (if not already authenticated)
gcloud auth login

# Set your project (replace with your actual project ID)
PROJECT_ID=$(gcloud config get-value project)
echo "Using project: $PROJECT_ID"

# If you need to set a different project:
# gcloud config set project YOUR_PROJECT_ID
```

### **1.2 Enable Required APIs**

```bash
# Enable all necessary APIs for deployment
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    containerregistry.googleapis.com \
    sqladmin.googleapis.com

echo "✅ APIs enabled successfully"
```

---

## **🐳 Phase 2: Optimize Application for Production (5 minutes)**

### **2.1 Update requirements.txt**

Ensure your `requirements.txt` includes all production dependencies:

```bash
cat > requirements.txt << 'EOF'
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
pydantic==2.5.3
pydantic-settings==2.1.0
python-dotenv==1.0.0
google-generativeai==0.3.2
pandas==2.1.4
psycopg2-binary==2.9.9
requests==2.31.0
EOF
```

### **2.2 Verify/Create Production Dockerfile**

Check your existing Dockerfile or create an optimized one:

```bash
cat > Dockerfile << 'EOF'
# ImaraFund Production Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 imarafund && chown -R imarafund:imarafund /app
USER imarafund

# Expose port 8080 (Cloud Run standard)
EXPOSE 8080

# Health check for monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
EOF
```

### **2.3 Prepare Environment Variables**

Extract your database connection details:

```bash
# Get your database password from .env file
DB_PASSWORD=$(grep DATABASE_URL .env | cut -d':' -f3 | cut -d'@' -f1)
GEMINI_KEY=$(grep GEMINI_API_KEY .env | cut -d'=' -f2)

echo "Database password extracted (verify it's correct): ${DB_PASSWORD:0:3}..."
echo "Gemini API key status: ${GEMINI_KEY:+Configured}"
```

---

## **🚀 Phase 3: Build and Deploy (10 minutes)**

### **3.1 Build Container Image**

```bash
# Build and push your application to Google Container Registry
gcloud builds submit --tag gcr.io/$PROJECT_ID/imarafund-api

# This takes 3-5 minutes and shows build progress
```

**Expected output:**

```
Creating temporary tarball archive...
Uploading tarball...
Starting Cloud Build...
DONE
SUCCESS
```

### **3.2 Deploy to Cloud Run**

**Replace the placeholder values below with your actual credentials:**

```bash
# Deploy with environment variables
gcloud run deploy imarafund-api \
    --image gcr.io/$PROJECT_ID/imarafund-api \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10 \
    --min-instances 0 \
    --set-env-vars "PROJECT_NAME=ImaraFund" \
    --set-env-vars "API_V1_PREFIX=/api/v1" \
    --set-env-vars "DEBUG=False" \
    --set-env-vars "DATABASE_URL=postgresql://imarafund_user:YOUR_DB_PASSWORD@35.187.125.154:5432/imarafund" \
    --set-env-vars "GEMINI_API_KEY=YOUR_GEMINI_KEY" \
    --set-env-vars "GEOGRAPHY_WEIGHT=0.40" \
    --set-env-vars "SECTOR_WEIGHT=0.30" \
    --set-env-vars "FUNDING_WEIGHT=0.20" \
    --set-env-vars "STAGE_WEIGHT=0.10"
```

**⚠️ Important:** Replace `YOUR_DB_PASSWORD` and `YOUR_GEMINI_KEY` with your actual values.

**Expected output:**

```
Deploying container to Cloud Run service [imarafund-api]...
✓ Deploying new service... Done.
Service [imarafund-api] revision [imarafund-api-00001] has been deployed.
Service URL: https://imarafund-api-xyz123-uc.a.run.app
```

---

## **✅ Phase 4: Production Verification (5 minutes)**

### **4.1 Get Your Production URL**

```bash
# Get your live service URL
SERVICE_URL=$(gcloud run services describe imarafund-api \
    --region us-central1 \
    --format 'value(status.url)')

echo "🎉 Your ImaraFund API is live at: $SERVICE_URL"
```

### **4.2 Comprehensive Testing**

```bash
# Test health endpoint
echo "Testing health check..."
curl $SERVICE_URL/health

# Test API root
echo "Testing API root..."
curl $SERVICE_URL/

# Test grants endpoint
echo "Testing grants data..."
curl "$SERVICE_URL/api/v1/grants?limit=3"

# Test companies endpoint
echo "Testing companies data..."
curl "$SERVICE_URL/api/v1/companies?limit=3"

# Test your matching algorithm (the main feature!)
echo "Testing intelligent matching algorithm..."
curl -X POST "$SERVICE_URL/api/v1/match/1?top_n=3"
```

### **4.3 Interactive Testing**

**Open these URLs in your browser:**

1. **🏠 API Root:** `https://your-service-url.run.app/`
2. **💚 Health Check:** `https://your-service-url.run.app/health`
3. **📚 Interactive Docs:** `https://your-service-url.run.app/docs` ⭐
4. **📖 Alternative Docs:** `https://your-service-url.run.app/redoc`

**The `/docs` endpoint provides a complete interactive interface for testing your 40/30/20/10 matching algorithm!**

---

## **🔒 Phase 5: Security and Monitoring**

### **5.1 Update Cloud SQL Security**

Your database needs to allow Cloud Run connections:

```bash
# Option 1: Allow Google Cloud services (recommended)
gcloud sql instances patch imarafund-db \
    --authorized-networks=0.0.0.0/0

# Note: For production, consider using Cloud SQL Proxy for enhanced security
```

### **5.2 Monitor Your Deployment**

```bash
# View real-time logs
gcloud run services logs tail imarafund-api --region us-central1

# View recent logs
gcloud run services logs read imarafund-api --region us-central1 --limit 50

# Check service status
gcloud run services describe imarafund-api --region us-central1
```

---

## **💰 Cost Management**

Your production deployment costs:

| **Service**            | **Configuration**    | **Monthly Cost** |
| ---------------------------- | -------------------------- | ---------------------- |
| **Cloud SQL**          | db-f1-micro (existing)     | $7-15                  |
| **Cloud Run**          | 1GB RAM, 1 CPU, auto-scale | $0-10                  |
| **Container Registry** | Image storage              | $0.26/GB               |
| **Networking**         | Data transfer              | $0.12/GB               |
| **Total Estimated**    |                            | **$10-30/month** |

**Cloud Run Free Tier Benefits:**

* 2 million requests/month
* 360,000 vCPU-seconds/month
* 180,000 GiB-seconds/month

**Cost Optimization:**

```bash
# Set scaling limits to control costs
gcloud run services update imarafund-api \
    --region us-central1 \
    --min-instances 0 \
    --max-instances 5
```

---

## **🛠️ Troubleshooting Guide**

### **Common Deployment Issues**

**1. “Container failed to start”**

```bash
# Check logs for specific error
gcloud run services logs read imarafund-api --region us-central1 --limit 20

# Common causes:
# - Wrong DATABASE_URL format
# - Missing psycopg2-binary in requirements.txt
# - Port not set to 8080
```

**2. “Database connection failed”**

```bash
# Verify Cloud SQL instance is running
gcloud sql instances describe imarafund-db

# Check authorized networks
gcloud sql instances describe imarafund-db --format="value(settings.ipConfiguration.authorizedNetworks)"

# Test connection string format:
# postgresql://user:password@host:5432/database
```

**3. “502 Bad Gateway”**

```bash
# Usually means app is not responding on port 8080
# Check Dockerfile CMD uses --port 8080
# Verify app/main.py starts correctly
```

### **Performance Issues**

```bash
# Increase memory if needed
gcloud run services update imarafund-api \
    --region us-central1 \
    --memory 2Gi

# Increase timeout for complex queries
gcloud run services update imarafund-api \
    --region us-central1 \
    --timeout 600
```

---

## **🎯 Production Success Checklist**

Run this comprehensive verification:

```python
# Save as production_test.py
import requests
import json

SERVICE_URL = "https://your-actual-service-url.run.app"  # Replace with your URL

print("🧪 ImaraFund Production Deployment Test\n")

tests = [
    ("Health Check", f"{SERVICE_URL}/health", "GET"),
    ("API Root", f"{SERVICE_URL}/", "GET"),
    ("List Grants", f"{SERVICE_URL}/api/v1/grants?limit=3", "GET"),
    ("List Companies", f"{SERVICE_URL}/api/v1/companies?limit=3", "GET"),
    ("Matching Algorithm", f"{SERVICE_URL}/api/v1/match/1?top_n=3", "POST"),
]

for name, url, method in tests:
    try:
        response = requests.request(method, url, timeout=30)
        if response.status_code == 200:
            print(f"✅ {name}: PASSED")
            if name == "Matching Algorithm":
                result = response.json()
                print(f"   Found {result['total_matches_found']} matches")
                if result['matches']:
                    top_match = result['matches'][0]
                    print(f"   Top match: {top_match['program_name']} ({top_match['match_score']}/100)")
        else:
            print(f"❌ {name}: FAILED (Status {response.status_code})")
    except Exception as e:
        print(f"❌ {name}: ERROR - {str(e)}")

print(f"\n🌐 Your ImaraFund API is live at: {SERVICE_URL}")
print(f"📚 Interactive docs: {SERVICE_URL}/docs")
```

---

## **🎉 Deployment Complete!**

### **Your Live Production System**

**🌐 Service URL:** `https://imarafund-api-[unique-id]-uc.a.run.app`

**Key Endpoints:**

* **Interactive API Docs:** `/docs` ⭐
* **Health Check:** `/health`
* **List Grants:** `/api/v1/grants`
* **Intelligent Matching:** `/api/v1/match/{company_id}`

### **What You’ve Achieved**

✅ **Global Accessibility:** Your API is now live on Google’s global infrastructure

✅ **Auto-Scaling:** Handles traffic spikes automatically (0-10 instances)

✅ **HTTPS Security:** Automatic SSL certificates and secure connections

✅ **Cost Efficiency:** Pay only for actual usage (~$10-30/month)

✅ **Production Database:** 103 grants and 50 companies ready for matching

✅ **AI Integration:** Gemini-powered recommendations available worldwide

✅ **Interactive Documentation:** Swagger UI accessible to stakeholders

### **Next Steps**

1. **Share Your API:** Send the `/docs` URL to stakeholders for testing
2. **Monitor Usage:** Check Cloud Console for traffic and performance metrics
3. **Custom Domain (Optional):**

```bash
   gcloud run domain-mappings create \
       --service imarafund-api \
       --domain api.yourdomain.com \
       --region us-central1
```

1. **Build Frontend:** Create a React/Vue.js app that calls your production API
2. **Add Authentication:** Implement API keys or OAuth for production security

**🚀 Your ImaraFund intelligent matching system is now live and serving the world! Test it at your production `/docs` endpoint and watch your 40/30/20/10 algorithm work with real data in the cloud.**

Ready to proceed with the deployment? Start with Phase 1 and let me know your results!
