
# 📘 ImaraFund Complete Team Handover & Deployment Guide

**AI-Powered Funding Matcher - Full System Documentation with Real Credentials**

---

## **🎯 Executive Summary**

This document provides everything needed for teammates to:

* **Immediately fix the `ai_advice: null` issue** (Gemini API quota problem)
* **Gain full owner access** to the Google Cloud project
* **Update code and redeploy** (algorithm weights, features, API keys)
* **Set up GitHub integration** for team collaboration
* **Recreate the entire system from scratch** using actual credentials

**Current Issue:** Your Gemini API free tier has hit quota limits, causing `"ai_advice": null` while `"ai_enabled": true`. This guide shows how to fix this immediately and prevent future issues.

---

## **🔐 Complete Credentials & Configuration (Real Data)**

⚠️ **Capstone Project Note:** These are the actual credentials for your live system. Share securely with teammates only.

### **Google Cloud Platform**

```yaml
Project ID: imarafund-capstone1
Project Name: ImaraFund Capstone
Project Number: 443679739700
Region: europe-west1 (Belgium)
Owner Email: elkomysarah7@gmail.com
Billing Account: 01C399-F59A6A-F14B8D
```

**Management URLs:**

* **Cloud Console:** [https://console.cloud.google.com/home/dashboard?project=imarafund-capstone1](https://console.cloud.google.com/home/dashboard?project=imarafund-capstone1)
* **Cloud Run Service:** [https://console.cloud.google.com/run/detail/europe-west1/imarafund-api?project=imarafund-capstone1](https://console.cloud.google.com/run/detail/europe-west1/imarafund-api?project=imarafund-capstone1)
* **Cloud SQL Instance:** [https://console.cloud.google.com/sql/instances/imarafund-db-v1/overview?project=imarafund-capstone1](https://console.cloud.google.com/sql/instances/imarafund-db-v1/overview?project=imarafund-capstone1)
* **IAM Management:** [https://console.cloud.google.com/iam-admin/iam?project=imarafund-capstone1](https://console.cloud.google.com/iam-admin/iam?project=imarafund-capstone1)

### **Database (Cloud SQL PostgreSQL)**

```yaml
Instance Name: imarafund-db-v1
Full Connection: imarafund-capstone1:europe-west1:imarafund-db-v1
Public IP: 130.211.88.95
Database: imarafund

# Application User (for Cloud Run)
Username: imarafund_user
Password: ImaraFund2024

# Admin User (for management)
Username: postgres  
Password: FreshStart2024!
```

**Connection Strings:**

```bash
# Local development
postgresql://imarafund_user:ImaraFund2024@130.211.88.95:5432/imarafund

# Cloud Run (Unix socket)
postgresql+psycopg2://imarafund_user:ImaraFund2024@/imarafund?host=/cloudsql/imarafund-capstone1:europe-west1:imarafund-db-v1
```

### **Google Gemini AI**

```yaml
Current API Key: AIzaSyCbPZ29ijBiAebd-ChRvkds2suYV3xblW8
Model: gemini-2.5-flash
Status: FREE TIER (Limited)

Free Tier Limits:
- 15 requests per minute
- 1,500 requests per day  
- 1 million tokens per day
```

### **Production Service**

```yaml
Base URL: https://imarafund-api-443679739700.europe-west1.run.app
Health Check: /health
Interactive Docs: /docs
Container Image: gcr.io/imarafund-capstone1/imarafund-api
```

---

## **🚨 IMMEDIATE FIX: Gemini API Quota Issue**

**Your Problem:** `"ai_advice": null` because free tier quota is exhausted.

**Why This Happens:**

* Free tier allows only **15 requests/minute** and **1,500/day**
* Your system generates AI advice for top 3 matches = 3 API calls per request
* After ~500 user requests, you hit the daily limit
* API calls fail silently, returning `null` instead of advice

### **Solution 1: Generate New API Key (Immediate Fix)**

**Step 1: Create New Gemini API Key**

1. Go to: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Click **“Create API Key”**
3. Select project: `imarafund-capstone1` or create new project
4. Copy the new key (starts with `AIzaSy...`)

**Step 2: Test New Key**

```bash
NEW_KEY="AIzaSy_YOUR_NEW_KEY_HERE"  # Replace with actual key

# Test immediately
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$NEW_KEY" \
    -H 'Content-Type: application/json' \
    -d '{"contents":[{"parts":[{"text":"Test"}]}]}' | jq
```

**Step 3: Update Cloud Run (No Code Changes Needed)**

```bash
# Update environment variable instantly
gcloud run services update imarafund-api \
    --region=europe-west1 \
    --project=imarafund-capstone1 \
    --update-env-vars "GEMINI_API_KEY=$NEW_KEY"

echo "✅ API key updated! Waiting 30 seconds for deployment..."
sleep 30

# Test immediately
curl -s "https://imarafund-api-443679739700.europe-west1.run.app/api/v1/match/1?top_n=1&include_ai_advice=true" -d "" | jq '.matches[0].ai_advice'
```

**Expected Result:** Should return AI advice text instead of `null`.

### **Solution 2: Reduce API Usage (Extend Quota)**

Edit the code to use fewer API calls:

**File: `app/main.py` (around line 180)**

```python
# Change from top 3 matches to top 1 match only
if i < 1:  # Changed from: if i < 3:
```

This reduces API usage by 66%, making your quota last 3x longer.

---

## **👥 Team Member Access Setup**

### **Grant Full Owner Access**

**Command Line Method (Fastest):**

```bash
# Replace with teammate's Gmail
TEAMMATE_EMAIL="teammate@gmail.com"

gcloud projects add-iam-policy-binding imarafund-capstone1 \
    --member="user:${TEAMMATE_EMAIL}" \
    --role="roles/owner"

echo "✅ ${TEAMMATE_EMAIL} added as project owner"

# Verify access
gcloud projects get-iam-policy imarafund-capstone1 \
    --flatten="bindings[].members" \
    --filter="bindings.role:roles/owner"
```

**Web Console Method:**

1. Go to: [https://console.cloud.google.com/iam-admin/iam?project=imarafund-capstone1](https://console.cloud.google.com/iam-admin/iam?project=imarafund-capstone1)
2. Click **“Grant Access”**
3. Enter teammate’s Gmail
4. Select role: **“Owner”**
5. Click **“Save”**

### **Teammate Setup Instructions**

Send these commands to your teammate:

```bash
# 1. Install Google Cloud SDK
# Download from: https://cloud.google.com/sdk/docs/install

# 2. Authenticate
gcloud auth login
# Sign in with their Gmail account

# 3. Configure project
gcloud config set project imarafund-capstone1
gcloud config set run/region europe-west1

# 4. Verify access
gcloud run services list
gcloud sql instances list

# 5. Test deployment access
gcloud run services describe imarafund-api --region=europe-west1
```

---

## **🔄 Code Update & Deployment Workflows**

### **Scenario 1: Change Algorithm Weights (Geography 40→50)**

**Step 1: Update Code Locally**

Edit `app/services/intelligent_matcher.py`:

```python
def _score_geography(self, company: Company, grant: Grant) -> float:
    """Score geographic eligibility (0-50 points) - UPDATED FROM 40"""
    company_country = str(company.nationality or '').lower().strip()
    grant_scope = str(grant.geographic_scope or '').lower().strip()
    grant_country = str(grant.country or '').lower().strip()

    # Global programs get full points
    if 'global' in grant_scope:
        return 50.0  # Changed from 40.0

    # Exact country match
    if company_country in grant_country or company_country in grant_scope:
        return 50.0  # Changed from 40.0

    # Regional matches
    africa_countries = ['nigeria', 'kenya', 'south africa', 'ghana', 'uganda', 'egypt']
    if company_country in africa_countries:
        if 'africa' in grant_scope or 'african' in grant_scope:
            return 43.75  # Proportionally increased from 35.0

    return 0.0

def _calculate_match_score(self, company: Company, grant: Grant) -> Tuple[float, Dict]:
    """Calculate match score with NEW 50/25/15/10 weighting"""
    score = 0.0
    breakdown = {}

    # Geographic: 50 points (was 40)
    geo_score = self._score_geography(company, grant)
    score += geo_score
    breakdown['geographic'] = float(geo_score)

    # Sector: 25 points (was 30) - scale down proportionally
    sector_score = self._score_sector(company, grant) * 0.833
    score += sector_score
    breakdown['sector'] = float(sector_score)

    # Funding: 15 points (was 20) - scale down proportionally  
    amount_score = self._score_funding_amount(company, grant) * 0.75
    score += amount_score
    breakdown['amount_fit'] = float(amount_score)

    # Stage: 10 points (unchanged)
    stage_score = self._score_business_stage(company, grant)
    score += stage_score
    breakdown['stage'] = float(stage_score)

    return min(100.0, score), breakdown
```

**Step 2: Test Locally**

```bash
# Run local server
uvicorn app.main:app --reload --port 8000

# Test changes
curl -s -X POST "http://localhost:8000/api/v1/match/1?top_n=1" -d "" | jq '.matches[0].score_breakdown'
```

**Expected Output:**

```json
{
  "geographic": 50,  // Changed from 40
  "sector": 25,      // Changed from 30
  "amount_fit": 15,  // Changed from 20
  "stage": 10        // Unchanged
}
```

**Step 3: Deploy to Production**

```bash
# Build new container (3-5 minutes)
gcloud builds submit \
    --tag gcr.io/imarafund-capstone1/imarafund-api \
    --project=imarafund-capstone1 \
    --timeout=20m

# Deploy to Cloud Run (30 seconds)
gcloud run deploy imarafund-api \
    --image gcr.io/imarafund-capstone1/imarafund-api \
    --region=europe-west1 \
    --project=imarafund-capstone1

echo "✅ Deployment complete!"
```

**Step 4: Verify in Production**

```bash
SERVICE_URL="https://imarafund-api-443679739700.europe-west1.run.app"

curl -s -X POST "${SERVICE_URL}/api/v1/match/1?top_n=1" -d "" | jq '{
    match_score: .matches[0].match_score,
    breakdown: .matches[0].score_breakdown
}'
```

### **Scenario 2: Update Environment Variables Only**

**Change Gemini Model:**

```bash
gcloud run services update imarafund-api \
    --region=europe-west1 \
    --project=imarafund-capstone1 \
    --update-env-vars "GEMINI_MODEL=gemini-1.5-flash"
```

**Update Multiple Variables:**

```bash
gcloud run services update imarafund-api \
    --region=europe-west1 \
    --project=imarafund-capstone1 \
    --set-env-vars "GEMINI_API_KEY=NEW_KEY,GEMINI_MODEL=gemini-1.5-flash,DEBUG=False"
```

---

## **🐙 GitHub Integration Setup**

### **Create Repository**

```bash
cd /d/D1/WTF/ImaraFund

# Initialize Git
git init

# Create .gitignore (IMPORTANT - excludes sensitive files)
cat > .gitignore << 'EOF'
# Environment files (never commit passwords!)
.env
.env.local
*.env

# Database files
*.db
*.sqlite
DB_CONNECTION_NAME.txt
DB_PUBLIC_IP.txt

# Python
__pycache__/
*.pyc
*.pyo
.Python
venv/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
EOF

# Initial commit
git add .
git commit -m "Initial commit: ImaraFund AI-powered funding matcher"

# Link to GitHub (create repo first on GitHub.com)
git remote add origin https://github.com/YOUR_USERNAME/ImaraFund.git
git branch -M main
git push -u origin main
```

### **Team Collaboration Workflow**

**Daily Workflow for Team Members:**

```bash
# 1. Pull latest changes
git pull origin main

# 2. Create feature branch
git checkout -b feature/update-weights

# 3. Make changes
# Edit files...

# 4. Test locally
uvicorn app.main:app --reload --port 8000

# 5. Commit changes
git add .
git commit -m "Update geography weight from 40 to 50 points"
git push origin feature/update-weights

# 6. Create Pull Request on GitHub
# Go to GitHub.com -> Create Pull Request -> Review -> Merge

# 7. Deploy to production
git checkout main
git pull origin main
gcloud builds submit --tag gcr.io/imarafund-capstone1/imarafund-api --project=imarafund-capstone1
gcloud run deploy imarafund-api --image gcr.io/imarafund-capstone1/imarafund-api --region=europe-west1 --project=imarafund-capstone1
```

### **Add Teammates as Collaborators**

**On GitHub:**

1. Go to: `https://github.com/YOUR_USERNAME/ImaraFund/settings/access`
2. Click **“Add people”**
3. Enter teammate’s GitHub username
4. Select **“Admin”** permission
5. Click **“Add to repository”**

**Teammate Setup:**

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ImaraFund.git
cd ImaraFund

# Set up environment
conda create -n imarafund python=3.12
conda activate imarafund
pip install -r requirements.txt

# Create local .env file (NOT committed to Git)
cat > .env << 'EOF'
DATABASE_URL=postgresql://imarafund_user:ImaraFund2024@130.211.88.95:5432/imarafund
GEMINI_API_KEY=AIzaSyCbPZ29ijBiAebd-ChRvkds2suYV3xblW8
GEMINI_MODEL=gemini-2.5-flash
EOF

# Test locally
uvicorn app.main:app --reload --port 8000
```

---

## **📋 Quick Reference Commands**

### **Most Common Operations**

**Update Gemini API Key:**

```bash
gcloud run services update imarafund-api \
    --region=europe-west1 \
    --project=imarafund-capstone1 \
    --update-env-vars "GEMINI_API_KEY=NEW_KEY"
```

**Deploy Code Changes:**

```bash
# Build and deploy (one-liner)
gcloud builds submit --tag gcr.io/imarafund-capstone1/imarafund-api --project=imarafund-capstone1 && gcloud run deploy imarafund-api --image gcr.io/imarafund-capstone1/imarafund-api --region=europe-west1 --project=imarafund-capstone1
```

**Check System Status:**

```bash
curl -s "https://imarafund-api-443679739700.europe-west1.run.app/health" | jq
```

**Test AI Functionality:**

```bash
curl -s -X POST "https://imarafund-api-443679739700.europe-west1.run.app/api/v1/match/1?top_n=1&include_ai_advice=true" -d "" | jq '.matches[0].ai_advice'
```

**View Logs:**

```bash
gcloud run services logs tail imarafund-api --region=europe-west1 --project=imarafund-capstone1
```

**Connect to Database:**

```bash
gcloud sql connect imarafund-db-v1 \
    --user=imarafund_user \
    --database=imarafund \
    --project=imarafund-capstone1
# Password: ImaraFund2024
```

**Add Team Member:**

```bash
gcloud projects add-iam-policy-binding imarafund-capstone1 \
    --member="user:teammate@gmail.com" \
    --role="roles/owner"
```

### **Emergency Reset Command**

If you need to completely reset the deployment:

```bash
gcloud run deploy imarafund-api \
    --image gcr.io/imarafund-capstone1/imarafund-api \
    --platform managed \
    --region europe-west1 \
    --project=imarafund-capstone1 \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --timeout 300 \
    --min-instances 1 \
    --max-instances 10 \
    --add-cloudsql-instances "imarafund-capstone1:europe-west1:imarafund-db-v1" \
    --set-env-vars "DATABASE_URL=postgresql+psycopg2://imarafund_user:ImaraFund2024@/imarafund?host=/cloudsql/imarafund-capstone1:europe-west1:imarafund-db-v1" \
    --set-env-vars "GEMINI_API_KEY=AIzaSyCbPZ29ijBiAebd-ChRvkds2suYV3xblW8" \
    --set-env-vars "GEMINI_MODEL=gemini-2.5-flash" \
    --set-env-vars "PROJECT_NAME=ImaraFund" \
    --set-env-vars "DEBUG=True"
```

---

## **🔧 Troubleshooting Guide**

| **Problem**          | **Cause**                    | **Solution**                                           |
| -------------------------- | ---------------------------------- | ------------------------------------------------------------ |
| `ai_advice: null`        | Gemini API quota exhausted         | Generate new API key and update with `--update-env-vars`   |
| `404`errors              | Database empty or connection issue | Run `python migrations/migrate_data.py`                    |
| Slow response times        | Cold start or no warm instances    | Set `--min-instances=1`                                    |
| Build failures             | Docker/dependency issues           | Check `requirements.txt`and `Dockerfile`                 |
| Permission denied          | Teammate not added as owner        | Run `gcloud projects add-iam-policy-binding`               |
| Database connection failed | IP address changed                 | Get new IP:`gcloud sql instances describe imarafund-db-v1` |

**Check Quota Status:**

```bash
# Look for quota errors in logs
gcloud run services logs read imarafund-api \
    --region=europe-west1 \
    --project=imarafund-capstone1 \
    --limit=100 | grep -E "(quota|429|rate limit)"
```

**Verify Environment Variables:**

```bash
gcloud run services describe imarafund-api \
    --region=europe-west1 \
    --project=imarafund-capstone1 \
    --format='yaml(spec.template.spec.containers[0].env)'
```

---

## **🎓 Summary**

This guide provides:

✅ **Immediate solution** to your `ai_advice: null` problem (Gemini API quota)

✅ **Complete credentials** for system recreation

✅ **Full team access setup** with owner permissions

✅ **Step-by-step deployment workflows** for code changes

✅ **GitHub integration** for version control and collaboration

✅ **Quick reference commands** for daily operations

✅ **Comprehensive troubleshooting** for common issues

**Your teammates can now:**

* Fix the AI quota issue immediately by generating new API keys
* Update algorithm weights and redeploy to production
* Collaborate using Git/GitHub workflows
* Manage the entire system independently
* Recreate the system from scratch if needed

**Next Steps:**

1. **Immediate:** Fix the AI issue using Section 3
2. **Team Setup:** Add teammates using Section 4
3. **Long-term:** Set up GitHub integration using Section 6
4. **Daily Use:** Reference Section 7 for common operations

**System Status:** ✅ **Production-Ready & Team-Collaborative**

---

**Document Version:** 2.0 (Complete Team Edition)

**Last Updated:** February 23, 2026

**Credentials:** ✅ Real credentials included for capstone project

**Team Ready:** ✅ Complete collaboration workflows included
