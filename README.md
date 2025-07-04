# KoNpLiAI

KoNpLiAI is a lightweight RegTech platform helping UK financial firms stay compliant with FCA, GDPR and SMCR regulations. Users upload policy documents which are analysed by Azure OpenAI. Results are logged immutably in Azure Confidential Ledger.

## Folder structure

```
backend/    FastAPI application
frontend/   React client built with Vite and TailwindCSS
.github/workflows/  CI/CD pipelines
.env.example  Sample environment configuration
```

## Deployment

These instructions assume Azure resources already exist in the resource group `RG_KonpliAI` located in `UK South`.

1. Copy `.env.example` to `.env` and fill in your Azure keys and endpoints.
2. Install backend requirements and run locally:
   ```bash
   pip install -r backend/requirements.txt
   uvicorn backend.main:app --reload
   ```
3. From `frontend` run:
   ```bash
   npm install
   npm run dev
   ```
4. Use the upload form to select a PDF or DOCX policy file. The backend will return a compliance summary, file hash and ledger link.

## CI/CD

Two GitHub Actions workflows deploy the application.

- `.github/workflows/backend.yml` deploys the FastAPI backend to Azure App Service `KoNpLiAI`.
- `.github/workflows/frontend.yml` deploys the React frontend to Azure Static Web Apps.

Both workflows authenticate with Azure using `azure/login` before deploying. Secrets required:

- `AZURE_CREDENTIALS` – JSON credentials for `azure/login`.
- `AZURE_WEBAPP_PUBLISH_PROFILE` – publish profile for the App Service.
- `AZURE_STATIC_WEB_APPS_API_TOKEN` – deployment token for Static Web Apps.

Once pushed to GitHub, the workflows will build and publish the latest code.
