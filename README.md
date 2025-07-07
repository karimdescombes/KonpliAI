# KoNpLiAI

Minimal SaaS MVP helping UK financial firms track FCA, GDPR and SMCR compliance. It uses Azure OpenAI to analyse uploaded policy documents and stores a record in Azure Confidential Ledger.

## Architecture

- **Backend**: FastAPI deployed to Azure App Service (`KoNpLiAI-Backend`)
- **Frontend**: React + Vite + Tailwind deployed to Azure Static Web Apps (`KoNpLiAI-Frontend`)
- **AI**: Azure OpenAI Service
- **Ledger**: Azure Confidential Ledger

Both apps reside in resource group `RG_KonpliAI` in the UK South region.

## Local development

1. Install Python 3.10+ and Node 18.
2. Copy `backend/.env.example` to `backend/.env` and add your Azure credentials.
3. Install backend dependencies:
   ```bash
   pip install fastapi uvicorn[standard] python-dotenv openai azure-confidentialledger azure-identity
   ```
4. Run the backend:
   ```bash
   uvicorn backend.main:app --reload
   ```
5. Install frontend dependencies:
   ```bash
   cd frontend && npm install
   npm run dev
   ```
6. Open `http://localhost:3000` to use the app.

## Azure provisioning

Create resources in the `RG_KonpliAI` resource group (UK South):

1. **Azure OpenAI** – create a resource and deployment (e.g. `gpt-35-turbo`).
2. **Azure Confidential Ledger** – note the ledger URI.
3. **App Service** – create `KoNpLiAI-Backend`.
4. **Static Web App** – create `KoNpLiAI-Frontend`.

## GitHub secrets

Set the following secrets for the workflows:

- `AZURE_WEBAPP_PUBLISH_PROFILE` – publish profile XML for the backend App Service.
- `AZURE_STATIC_WEB_APPS_API_TOKEN` – deployment token for the Static Web App.
- `AZURE_CREDENTIALS` – JSON credentials for `azure/login@v1`.

## Deployment

Pushing changes under `backend/` or `frontend/` triggers the respective GitHub Actions workflows which deploy automatically to Azure.

