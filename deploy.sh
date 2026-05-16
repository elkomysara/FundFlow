#!/bin/bash
# ImaraFund Cloud Run Deployment Script

PROJECT_ID="your-project-id"
SERVICE_NAME="imarafund-api"
REGION="us-central1"

echo "🚀 Deploying ImaraFund to Google Cloud Run"
echo "Project: $PROJECT_ID"
echo "Service: $SERVICE_NAME"
echo "Region: $REGION"
echo ""

# Build and submit to Cloud Build
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars "PROJECT_NAME=ImaraFund" \
    --set-env-vars "DEBUG=False"

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your API URL:"
gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)"