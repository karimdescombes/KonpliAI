import json
import os
import hashlib
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import openai
from azure.confidentialledger import ConfidentialLedgerClient
from azure.identity import DefaultAzureCredential

load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
LEDGER_URI = os.getenv("AZURE_CONFIDENTIAL_LEDGER_URI")

app = FastAPI(title="KoNpLiAI Backend")


async def summarise_document(content: bytes) -> str:
    """Call Azure OpenAI to summarise the uploaded document."""
    if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_ENDPOINT:
        raise RuntimeError("Azure OpenAI credentials not configured")

    openai.api_key = AZURE_OPENAI_API_KEY
    openai.base_url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments"  # Azure style
    # This assumes a deployment named 'gpt-35-turbo'. Adjust if different.
    response = openai.chat.completions.create(
        model="gpt-35-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a compliance assistant summarising UK regulatory obligations for FCA, GDPR and SMCR."
            },
            {
                "role": "user",
                "content": content.decode(errors="ignore")[:4000]
            },
        ],
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()


async def log_to_ledger(summary: str, digest: str) -> str:
    """Write the summary and hash to Azure Confidential Ledger and return the proof URL."""
    if not LEDGER_URI:
        raise RuntimeError("Ledger URI not configured")
    credential = DefaultAzureCredential()
    client = ConfidentialLedgerClient(ledger_endpoint=LEDGER_URI, credential=credential)
    entry = json.dumps({"summary": summary, "sha256": digest})
    receipt = client.create_ledger_entry(entry)
    tx_id = receipt["transactionId"]
    return f"{LEDGER_URI}/app/transactions/{tx_id}"


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    """Handle policy document upload and return compliance summary."""
    if file.content_type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]:
        raise HTTPException(status_code=400, detail="Only PDF or DOCX files are allowed")

    content = await file.read()
    digest = hashlib.sha256(content).hexdigest()
    summary = await summarise_document(content)
    ledger_url = await log_to_ledger(summary, digest)
    return JSONResponse({"summary": summary, "sha256": digest, "ledger_url": ledger_url})
