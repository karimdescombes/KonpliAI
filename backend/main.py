from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import os
from dotenv import load_dotenv
import openai
from azure.identity import DefaultAzureCredential
from azure.confidentialledger import ConfidentialLedgerClient

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")

ledger_endpoint = os.getenv("AZURE_LEDGER_ENDPOINT")


def save_file(file: UploadFile, content: bytes) -> str:
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as f:
        f.write(content)
    return path


def compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def analyse_text(text: str) -> str:
    prompt = (
        "Analyse the following policy document for FCA, GDPR, and SMCR compliance gaps. "
        "Provide a concise summary of any issues."
    )
    try:
        response = openai.ChatCompletion.create(
            engine="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
        )
        return response.choices[0].message["content"]
    except Exception:
        return "AI analysis could not be completed."


def log_to_ledger(entry: str) -> str:
    try:
        credential = DefaultAzureCredential()
        client = ConfidentialLedgerClient(ledger_endpoint, credential)
        result = client.create_entry({"contents": entry})
        txn = result["transactionId"]
        return f"{ledger_endpoint}/app/transactions/{txn}"
    except Exception:
        return "Ledger write failed."


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    sha256 = compute_sha256(content)
    save_file(file, content)
    text = content.decode(errors="ignore")
    summary = analyse_text(text)
    ledger_url = log_to_ledger(summary)
    return {"summary": summary, "sha256": sha256, "ledger_url": ledger_url}
