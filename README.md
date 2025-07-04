# KoNpLiAI

A minimal RegTech SaaS platform helping UK financial firms comply with FCA, GDPR and SMCR.

## Folder structure

```
backend/       FastAPI service
frontend/      React + Vite + Tailwind UI
infra/         (optional) Bicep templates
.github/
  workflows/   CI/CD pipelines
```

## Backend

Run locally:

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Environment variables are listed in `.env.example`.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Deployment

### Azure Web App (FastAPI)
1. Create an Azure Web App with a Linux runtime.
2. Configure the secrets `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_KEY`, `AZURE_OPENAI_DEPLOYMENT`, and `LEDGER_ENDPOINT`.
3. GitHub Actions workflow `backend.yml` deploys on pushes to `main`.

### Azure Static Web App (React)
1. Create a Static Web App in Azure.
2. Add deployment token as `AZURE_STATIC_WEB_APPS_API_TOKEN` secret.
3. Workflow `frontend.yml` builds and deploys the React app.

## Usage
Upload a policy document via the web interface or POST `/analyse` with a file. The API returns a summary, SHA-256 hash and a link to the ledger proof if available.
