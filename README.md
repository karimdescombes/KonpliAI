# KonpliAI

KonpliAI is a minimal RegTech platform helping UK financial firms stay compliant with FCA, GDPR and SMCR regulations.

## Folder structure

```
backend/   # FastAPI application
frontend/  # React + Vite + TailwindCSS app
infra/     # Optional Bicep templates
.github/workflows/  # CI/CD pipelines
```

## Backend

The FastAPI service exposes a single `/analyse` endpoint which accepts a policy document (PDF or Word), sends the content to Azure OpenAI for analysis, computes a SHA256 hash and logs a short entry to Azure Confidential Ledger. The API returns the compliance summary, document hash and a URL to verify the ledger transaction.

### Local development

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Environment variables are loaded from `.env` – see `.env.example` for values to provide.

## Frontend

A simple React interface allows document upload and displays the response from the backend.

### Local development

```bash
cd frontend
npm install
npm run dev
```

## Deployment

Resources are expected in the Azure region **UK South** within resource group **RG_KonpliAI**. See `infra/main.bicep` as a starting point for provisioning.

GitHub Actions workflows automate deployments:

- **backend.yml** – deploys the FastAPI backend to Azure App Service.
- **frontend.yml** – deploys the React frontend to Azure Static Web App.

Both workflows authenticate with Azure using the `azure/login` action before any deployment step. Required secrets:

- `AZURE_CREDENTIALS` – service principal credentials in JSON.
- `AZURE_WEBAPP_PUBLISH_PROFILE` – publish profile for the App Service.
- `AZURE_WEBAPP_NAME` – name of the App Service.
- `AZURE_STATIC_WEB_APPS_PUBLISH_PROFILE` – deployment token for the Static Web App.

Configure these secrets in your GitHub repository and push to deploy.
