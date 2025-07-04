from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from hashlib import sha256
from azure.identity import DefaultAzureCredential
from azure.confidentialledger import ConfidentialLedgerClient
from azure.core.exceptions import HttpResponseError
import openai
import os
import tempfile

app = FastAPI(title="KoNpLiAI Backend")

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
LEDGER_ENDPOINT = os.getenv("LEDGER_ENDPOINT")

if not AZURE_OPENAI_ENDPOINT:
    raise RuntimeError("AZURE_OPENAI_ENDPOINT not configured")

openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_key = AZURE_OPENAI_KEY

cred = DefaultAzureCredential()
ledger_client = ConfidentialLedgerClient(LEDGER_ENDPOINT, cred) if LEDGER_ENDPOINT else None

async def analyse_document(content: bytes) -> str:
    """Send document content to Azure OpenAI for analysis."""
    prompt = (
        "You are a compliance assistant for UK financial regulations (FCA, GDPR, SMCR). "
        "Read the following document and provide a short summary of compliance gaps."
    )
    response = openai.ChatCompletion.create(
        deployment_id=AZURE_OPENAI_DEPLOYMENT,
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": content.decode("utf-8", errors="ignore")}],
        temperature=0.2,
    )
    return response["choices"][0]["message"]["content"].strip()

@app.post("/analyse")
async def analyse(file: UploadFile = File(...)):
    if file.content_type not in ("application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    data = await file.read()
    summary = await analyse_document(data)
    doc_hash = sha256(data).hexdigest()

    entry_url = None
    if ledger_client:
        try:
            entry = ledger_client.create_ledger_entry(contents=doc_hash)
            entry_url = f"{LEDGER_ENDPOINT}/app/transactions/{entry.transaction_id}"
        except HttpResponseError:
            entry_url = None

    return JSONResponse({
        "summary": summary,
        "hash": doc_hash,
        "proof_link": entry_url,
    })
