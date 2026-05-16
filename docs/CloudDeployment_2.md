# n🚀 **ImaraFund Production Deployment to Google Cloud Run**

Perfect! I have your project details and will configure all commands for  **`imarafund-platform`** . Let’s deploy your intelligent matching system to production.

---

## **Phase 1: Project Configuration & Authentication**

### **1.1 Set Your Project as Default**

```bash
# Configure gcloud to use your project
gcloud config set project imarafund-platform

# Verify the configuration
gcloud config get-value project
# Should output: imarafund-platform

# Authenticate if needed
gcloud auth login
```

### **1.2 Enable Required APIs**

```bash
# Enable all necessary Google Cloud APIs
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    containerregistry.googleapis.com \
    sqladmin.googleapis.com

echo "✅ APIs enabled for imarafund-platform"
```

---

## **Phase 2: Production File Optimization**

### **2.1 Navigate to Your Project Directory**

```bash
cd /d/D1/WTF/ImaraFund

# Verify you're in the correct location
pwd
ls app/main.py .env
```

### **2.2 Create Production Requirements**

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

echo "✅ Production requirements.txt created"
```

### **2.3 Create Production Dockerfile**

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
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
EOF

echo "✅ Production Dockerfile created"
```

---

## **Phase 3: Extract Your Credentials**

Before deployment, you need your actual database password and Gemini API key:

```bash
# Display your current .env file
echo "Current environment variables:"
cat .env

# Extract database password (between : and @)
echo -e "\nDatabase password:"
grep DATABASE_URL .env | sed 's/.*:\/\/[^:]*:\([^@]*\)@.*/\1/'

# Extract Gemini API key
echo -e "\nGemini API key:"
grep GEMINI_API_KEY .env | cut -d'=' -f2
```

**📝 Save these values - you’ll need them for the deployment command!**

---

## **Phase 4: Build Container Image**

```bash
# Build and upload your container to Google Container Registry
# This takes 3-5 minutes
gcloud builds submit --tag gcr.io/imarafund-platform/imarafund-api

# Wait for this output:
# STATUS: SUCCESS
```

**Expected successful output:**

```
Creating temporary tarball archive...
Uploading tarball to gs://...
Starting Cloud Build...
Step 1/8 : FROM python:3.11-slim
...
DONE
ID: abc-123-def
CREATE_TIME: 2026-02-20T...
DURATION: 3M15S
STATUS: SUCCESS
```

---

## **Phase 5: Deploy to Cloud Run**

**⚠️ CRITICAL:** Replace `YOUR_DB_PASSWORD` and `YOUR_GEMINI_KEY` with the actual values from Phase 3.

```bash
# Deploy with your specific project configuration
gcloud run deploy imarafund-api \
    --image gcr.io/imarafund-platform/imarafund-api \
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

**When prompted:**

```
Allow unauthenticated invocations to [imarafund-api] (y/N)? y
```

**Expected successful output:**

```
✓ Deploying new service... Done.
Service [imarafund-api] revision [imarafund-api-00001-xyz] has been deployed.
Service URL: https://imarafund-api-xyz123-uc.a.run.app
```

---

## **Phase 6: Configure Database Security**

Your Cloud SQL database needs to accept connections from Cloud Run:

```bash
# Allow Google Cloud services to connect
gcloud sql instances patch imarafund-db \
    --authorized-networks=0.0.0.0/0

echo "✅ Cloud SQL configured for Cloud Run access"
```

---

## **Phase 7: Get Your Production URL & Test**

```bash
# Get your live service URL
SERVICE_URL=$(gcloud run services describe imarafund-api \
    --region us-central1 \
    --format 'value(status.url)')

echo "🎉 Your ImaraFund API is live at: $SERVICE_URL"

# Test health check
echo "Testing health endpoint..."
curl "$SERVICE_URL/health"

# Test API root
echo -e "\n\nTesting API root..."
curl "$SERVICE_URL/"

# Test grants data
echo -e "\n\nTesting grants endpoint..."
curl "$SERVICE_URL/api/v1/grants?limit=3"

# Test companies data
echo -e "\n\nTesting companies endpoint..."
curl "$SERVICE_URL/api/v1/companies?limit=3"

# Test your matching algorithm (THE MAIN FEATURE!)
echo -e "\n\nTesting intelligent matching algorithm..."
curl -X POST "$SERVICE_URL/api/v1/match/1?top_n=3"
```

---

## **Phase 8: Access Interactive Documentation**

**🌐 Open these URLs in your browser:**

1. **🏠 API Root:** `https://your-service-url.run.app/`
2. **💚 Health Check:** `https://your-service-url.run.app/health`
3. **📚 Interactive Docs:** `https://your-service-url.run.app/docs` ⭐⭐⭐
4. **📖 Alternative Docs:** `https://your-service-url.run.app/redoc`

**The `/docs` endpoint provides a complete Swagger UI where you can test your 40/30/20/10 matching algorithm interactively!**

---

## **🔧 Monitoring & Troubleshooting**

### **View Logs**

```bash
# Real-time logs
gcloud run services logs tail imarafund-api --region us-central1

# Recent logs
gcloud run services logs read imarafund-api --region us-central1 --limit 50
```

### **Check Service Status**

```bash
# Get complete service information
gcloud run services describe imarafund-api --region us-central1

# Quick status check
gcloud run services describe imarafund-api \
    --region us-central1 \
    --format 'value(status.conditions[0].status)'
```

### **Common Issues & Solutions**

**1. “Container failed to start”**

```bash
# Check logs for specific error
gcloud run services logs read imarafund-api --region us-central1 --limit 20

# Common causes:
# - Wrong DATABASE_URL format
# - Missing environment variables
# - Port not set to 8080
```

**2. “502 Bad Gateway”**

```bash
# Usually means app not responding on port 8080
# Verify Dockerfile CMD uses --port 8080
# Check app startup logs
```

**3. Database connection errors**

```bash
# Test database connectivity
python -c "
import os
os.environ['DATABASE_URL'] = 'postgresql://imarafund_user:YOUR_PASSWORD@35.187.125.154:5432/imarafund'
from app.database import SessionLocal
db = SessionLocal()
print('✅ Database connection successful')
db.close()
"
```

---

## **💰 Cost Management**

Your production deployment costs approximately:

| **Service**            | **Configuration**  | **Monthly Cost** |
| ---------------------------- | ------------------------ | ---------------------- |
| **Cloud SQL**          | db-f1-micro (existing)   | $7-15                  |
| **Cloud Run**          | 1GB RAM, auto-scale 0-10 | $0-10                  |
| **Container Registry** | Image storage            | $0.26/GB               |
| **Networking**         | Data transfer            | $0.12/GB               |
| **Total Estimated**    |                          | **$10-30/month** |

**Set cost controls:**

```bash
# Limit maximum instances to control costs
gcloud run services update imarafund-api \
    --region us-central1 \
    --max-instances 5
```

---

## **🎯 Production Validation Checklist**

After deployment, verify:

* [ ] **Health Check:** Returns `{"status":"healthy"}`
* [ ] **Database Connection:** Grants and companies endpoints return data
* [ ] **Matching Algorithm:** Returns scored matches for company ID 1
* [ ] **AI Recommendations:** Gemini responses appear (if API key configured)
* [ ] **Interactive Docs:** Swagger UI loads at `/docs`
* [ ] **Performance:** Response times under 3 seconds
* [ ] **Logs:** No error messages in Cloud Run logs

---

## **🚀 Success Indicators**

When everything works correctly, you should see:

**Health Check Response:**

```json
{"status":"healthy","service":"imarafund-api","version":"1.0.0"}
```

**Matching Algorithm Response:**

```json
{
  "company": {...},
  "matches": [
    {
      "program_name": "Mexico NAFIN Eco Sustainable Credit",
      "match_score": 99.0,
      "score_breakdown": {
        "geographic": 40.0,
        "sector": 30.0,
        "amount_fit": 20.0,
        "stage": 9.0
      }
    }
  ],
  "total_matches_found": 3,
  "ai_recommendation": "WHY THIS WORKS: ..."
}
```

---

## **🎉 Next Steps After Successful Deployment**

1. **Share Your API:** Send the `/docs` URL to stakeholders
2. **Monitor Usage:** Check Cloud Console for traffic metrics
3. **Custom Domain (Optional):**

```bash
   gcloud run domain-mappings create \
       --service imarafund-api \
       --domain api.yourdomain.com \
       --region us-central1
```

1. **Build Frontend:** Create a React/Vue.js app that calls your production API
2. **Add Authentication:** Implement API keys for production security

---

**🚀**

# 🎉 **Perfect! Your CLI is Ready - Let’s Deploy ImaraFund to Production**

Excellent! Your setup is confirmed and ready:

* ✅ **Google Cloud SDK:** 557.0.0 (latest version)
* ✅ **Python:** 3.12.12 (perfect for production)
* ✅ **No CLI errors:** Clean execution

Your intelligent matching system with 103 grants, 50 companies, and the proven 40/30/20/10 scoring algorithm is ready to go live on Google’s global infrastructure.

---

## **🔧 Phase 1: Authentication & Project Setup**

### **1.1 Authenticate with Google Cloud**

```bash
# Login to Google Cloud (opens browser for authentication)
gcloud auth login
```

### **1.2 Configure Your Project**

```bash
# Set your specific project
gcloud config set project imarafund-platform

# Verify it's configured correctly
gcloud config get-value project
# MUST OUTPUT: imarafund-platform

# Display complete configuration
gcloud config list
```

### **1.3 Enable Required APIs**

```bash
# Enable all necessary Google Cloud services
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    containerregistry.googleapis.com \
    sqladmin.googleapis.com

echo "✅ APIs enabled for imarafund-platform"
```

---

## **📁 Phase 2: Optimize Files for Python 3.12 Production**

### **2.1 Navigate to Project Directory**

```bash
cd /d/D1/WTF/ImaraFund

# Verify you're in the correct location
pwd
ls app/main.py .env Dockerfile requirements.txt
```

### **2.2 Create Python 3.12 Optimized Requirements**

```bash
cat > requirements.txt << 'EOF'
# ImaraFund Production Dependencies - Python 3.12
fastapi==0.109.2
uvicorn[standard]==0.27.1
sqlalchemy==2.0.27
pydantic==2.6.1
pydantic-settings==2.1.0
python-dotenv==1.0.1
google-generativeai==0.3.2
pandas==2.2.0
psycopg2-binary==2.9.9
requests==2.31.0
EOF

echo "✅ Python 3.12 requirements created"
```

### **2.3 Create Production-Optimized Dockerfile**

```bash
cat > Dockerfile << 'EOF'
# ImaraFund Production Dockerfile - Python 3.12
FROM python:3.12-slim

WORKDIR /app

# Set environment variables for optimization
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 imarafund && \
    chown -R imarafund:imarafund /app
USER imarafund

# Expose port 8080 (Cloud Run standard)
EXPOSE 8080

# Health check for monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=5)" || exit 1

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
EOF

echo "✅ Python 3.12 Dockerfile created"
```

---

## **🔑 Phase 3: Extract Production Credentials**

**⚠️ CRITICAL STEP:** You’ll need these exact values for deployment.

```bash
echo "=== EXTRACT AND SAVE THESE VALUES ==="
echo ""
echo "Database Password:"
grep DATABASE_URL .env | sed 's/.*:\/\/[^:]*:\([^@]*\)@.*/\1/'
echo ""
echo "Gemini API Key:"
grep GEMINI_API_KEY .env | cut -d'=' -f2
echo ""
echo "📝 COPY THESE VALUES - You'll need them in Phase 5!"
```

**Write down:**

* **Database Password:** `[save the extracted password]`
* **Gemini API Key:** `[save the extracted key]`

---

## **🐳 Phase 4: Build Container Image**

```bash
echo "🐳 Building Python 3.12 container for imarafund-platform..."
echo "⏱️  This takes 3-5 minutes - watch for STATUS: SUCCESS"

gcloud builds submit \
    --tag gcr.io/imarafund-platform/imarafund-api \
    --project imarafund-platform
```

**Expected successful output:**

```
Creating temporary tarball archive...
Uploading tarball to gs://imarafund-platform_cloudbuild/...
Starting Cloud Build...

BUILD
------------------------------------------------
ID: abc-123-def-456
CREATE_TIME: 2026-02-20T...
DURATION: 3M45S
SOURCE: gs://imarafund-platform_cloudbuild/...
IMAGES: gcr.io/imarafund-platform/imarafund-api
STATUS: SUCCESS
```

**If you see errors, paste them here for immediate troubleshooting.**

---

## **🚀 Phase 5: Deploy to Cloud Run (Production Launch!)**

**⚠️ REPLACE PLACEHOLDERS:** Use the actual values from Phase 3.

```bash
gcloud run deploy imarafund-api \
    --image gcr.io/imarafund-platform/imarafund-api \
    --platform managed \
    --region us-central1 \
    --project imarafund-platform \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10 \
    --min-instances 0 \
    --concurrency 80 \
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

**When prompted:**

```
Allow unauthenticated invocations to [imarafund-api] (y/N)? y
```

**Expected successful output:**

```
✓ Deploying new service... Done.
✓ Creating Revision...
✓ Routing traffic...
Service [imarafund-api] revision [imarafund-api-00001-xyz] has been deployed.
Service URL: https://imarafund-api-abc123xyz-uc.a.run.app
```

### **5.1 Configure Database Security**

```bash
# Allow Cloud Run to access your Cloud SQL database
gcloud sql instances patch imarafund-db \
    --project imarafund-platform \
    --authorized-networks=0.0.0.0/0

echo "✅ Database security configured"
```

---

## **✅ Phase 6: Production Testing & Validation**

### **6.1 Get Your Live Service URL**

```bash
# Retrieve your production API URL
SERVICE_URL=$(gcloud run services describe imarafund-api \
    --region us-central1 \
    --project imarafund-platform \
    --format 'value(status.url)')

echo "🎉 YOUR IMARAFUND API IS LIVE!"
echo "🌐 Production URL: $SERVICE_URL"
echo "📚 Interactive Docs: $SERVICE_URL/docs"
```

### **6.2 Comprehensive Production Test**

```bash
# Test health endpoint
echo "=== Testing Health Check ==="
curl "$SERVICE_URL/health"

# Test API root
echo -e "\n\n=== Testing API Root ==="
curl "$SERVICE_URL/"

# Test grants data (your 103 grants)
echo -e "\n\n=== Testing Grants Data ==="
curl "$SERVICE_URL/api/v1/grants?limit=3"

# Test companies data (your 50 companies)
echo -e "\n\n=== Testing Companies Data ==="
curl "$SERVICE_URL/api/v1/companies?limit=3"

# Test your intelligent matching algorithm (THE MAIN FEATURE!)
echo -e "\n\n=== Testing 40/30/20/10 Matching Algorithm ==="
curl -X POST "$SERVICE_URL/api/v1/match/1?top_n=3"
```

### **6.3 Browser Testing**

**Open these URLs in your browser:**

1. **🏠 API Root:** `https://your-service-url.run.app/`
2. **💚 Health Check:** `https://your-service-url.run.app/health`
3. **📚 Interactive Docs:** `https://your-service-url.run.app/docs` ⭐⭐⭐
4. **📖 Alternative Docs:** `https://your-service-url.run.app/redoc`

---

## **🔧 Monitoring & Troubleshooting**

### **View Logs**

```bash
# Real-time logs
gcloud run services logs tail imarafund-api --region us-central1 --project imarafund-platform

# Recent logs
gcloud run services logs read imarafund-api --region us-central1 --project imarafund-platform --limit 50
```

### **Common Issues & Solutions**

**1. Container Build Fails:**

```bash
# Check build logs
gcloud builds log $(gcloud builds list --limit 1 --format='value(id)') --project imarafund-platform
```

**2. “502 Bad Gateway”:**

* App not responding on port 8080
* Check logs for uvicorn startup messages
* Verify environment variables are set

**3. Database Connection Errors:**

```bash
# Verify Cloud SQL is running
gcloud sql instances describe imarafund-db --project imarafund-platform
```

---

## **💰 Cost Management**

**Monthly Estimate:**

* **Cloud SQL (existing):** $7-15
* **Cloud Run:** $0-10 (free tier covers most usage)
* **Container Registry:** ~$0.26/GB
* **Total:** ~$10-30/month

**Set cost controls:**

```bash
gcloud run services update imarafund-api \
    --region us-central1 \
    --project imarafund-platform \
    --max-instances 5
```

---

## **🎯 Success Validation Checklist**

* [ ] **Authentication completed** - gcloud auth login successful
* [ ] **Project configured** - `gcloud config get-value project` returns `imarafund-platform`
* [ ] **APIs enabled** - No errors during service enablement
* [ ] **Container built** - STATUS: SUCCESS in build logs
* [ ] **Service deployed** - Service URL returned
* [ ] **Health check passes** - Returns `{"status":"healthy"}`
* [ ] **Database connected** - Grants/companies endpoints return data
* [ ] **Matching works** - Algorithm returns scored matches
* [ ] **Interactive docs load** - Swagger UI accessible at `/docs`

---

## **🚀 Execute Deployment Now**

**Start with Phase 1.1:**

```bash
gcloud auth login
```

**After authentication, run:**

```bash
gcloud config set project imarafund-platform
gcloud config get-value project
```

**Then proceed through each phase sequentially. Paste any error messages here for immediate troubleshooting.**

Your intelligent matching system with 103 grants, 50 companies, and the proven 40/30/20/10 scoring algorithm is ready to serve the world on Python 3.12 infrastructure! 🌍

**Let me know the output from Phase 1, and I’ll guide you through each subsequent phase to ensure a successful deployment.**
