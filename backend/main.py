import hashlib
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai
from azure.confidentialledger import ConfidentialLedgerClient
from azure.identity import DefaultAzureCredential

app = FastAPI(title="KonpliAI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Azure OpenAI
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Configure Azure Confidential Ledger
LEDGER_URL = os.getenv("AZURE_LEDGER_URL")
credential = DefaultAzureCredential()
ledger_client = ConfidentialLedgerClient(ledger_url=LEDGER_URL, credential=credential)

@app.post("/analyse")
async def analyse(file: UploadFile = File(...)):
    """Upload a policy document and return compliance summary, SHA256 hash and ledger proof."""
    if file.content_type not in [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    data = await file.read()
    sha256 = hashlib.sha256(data).hexdigest()

    # Call Azure OpenAI to analyse document content
    prompt = (
        "You are a compliance officer for UK financial firms. "
        "Analyse the following policy text and summarise any gaps with FCA, GDPR and SMCR regulations."
    )
    response = openai.ChatCompletion.create(
        engine=DEPLOYMENT,
        messages=[{"role": "user", "content": prompt + "\n\n" + data.decode(errors="ignore")[:5000]}],
        temperature=0,
    )
    summary = response.choices[0].message.content.strip()

    # Write hash and summary fragment to ledger for audit-proof traceability
    entry = ledger_client.create_ledger_entry(
        contents=f"hash:{sha256};summary:{summary[:200]}"
    )
    tx_id = entry["transaction_id"]
    proof_url = f"{LEDGER_URL}/app/transactions/{tx_id}"

    return {"summary": summary, "sha256": sha256, "ledger_url": proof_url}

