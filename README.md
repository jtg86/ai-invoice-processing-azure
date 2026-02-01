# AI Invoice Processing in Azure

This project demonstrates how artificial intelligence can be used to automate invoice processing for public sector organizations using Microsoft Azure.

The solution uses Azure AI Document Intelligence to extract structured data from invoices, serverless Azure Functions for processing, and Azure OpenAI for intelligent accounting suggestions.

The project is designed with GDPR, traceability, and human-in-the-loop principles in mind, making it suitable for municipalities and shared service providers.

> **Disclaimer**
> This repository is a demonstration and portfolio project and is not intended as a production-ready financial system.

## 🧠 Project idea (short)

A system that:

- Receives invoices (PDF/scans)
- Uses AI to read and understand content
- Validates data automatically
- Suggests accounting classifications
- Sends to approval or ERP system

## 🏗️ Architecture overview

Flow:

1. Invoice uploaded → Azure Blob Storage
2. Azure Function triggered
3. AI reads invoice (Document Intelligence)
4. Data structured + validated
5. Result sent to approval/ERP via Logic Apps

### ☁️ Azure services used

| Service | Purpose |
| --- | --- |
| Azure Blob Storage | Invoice storage |
| Azure AI Document Intelligence | Invoice extraction |
| Azure Functions | Serverless processing |
| Azure OpenAI | Accounting suggestions |
| Azure Logic Apps | Workflow/integration |
| Entra ID | Authentication & RBAC |
| Application Insights | Logging & traceability |

## 📂 Repository structure

```
ai-invoice-processing-azure/
│
├── infrastructure/
│   ├── main.bicep
│   └── parameters.json
│
├── functions/
│   ├── process_invoice/
│   │   ├── __init__.py
│   │   └── function.json
│   │
│   └── suggest_accounting/
│       ├── __init__.py
│       └── function.json
│
├── sample-invoices/
│   └── example_invoice.pdf
│
├── output/
│   └── parsed_invoice.json
│
├── README.md
└── SECURITY.md
```

## 🧾 Azure Function – invoice processing

The `process_invoice` function is a real implementation using Azure AI Document Intelligence (prebuilt invoice model). It extracts structured data and writes the result to Blob Storage.

```python
import json
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["FORM_RECOGNIZER_ENDPOINT"]
key = os.environ["FORM_RECOGNIZER_KEY"]

def main(blob: bytes):
    client = DocumentAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    poller = client.begin_analyze_document(
        model_id="prebuilt-invoice",
        document=blob
    )

    result = poller.result()

    invoice = result.documents[0].fields

    parsed = {
        "supplier": invoice["VendorName"].value if "VendorName" in invoice else None,
        "invoiceNumber": invoice["InvoiceId"].value,
        "invoiceDate": str(invoice["InvoiceDate"].value),
        "totalAmount": invoice["InvoiceTotal"].value.amount,
        "currency": invoice["InvoiceTotal"].value.currency,
        "confidence": result.confidence
    }

    return json.dumps(parsed, indent=2)
```

## 🤖 AI – accounting suggestions (Azure OpenAI)

**Example prompt:**

```
You are an accounting assistant for a Norwegian municipality.

Invoice details:
Supplier: Telenor ASA
Description: Mobile subscriptions for employees
Total: 12,480 NOK

Suggest:
- Account number
- Cost center
- Justification
```

**Example output:**

```json
{
  "account": "6900",
  "costCenter": "IKT-Drift",
  "reason": "Telecommunication services"
}
```

## 👤 Human-in-the-loop

A Power App (or any low-code UI) can display:

- Original invoice
- AI extraction
- Accounting suggestion
- Confidence score

Actions:

- Approve
- Send to attestation
- Reject

## 🔐 Security & GDPR

See [SECURITY.md](SECURITY.md) for the full security posture, including:

- Data residency in Norway East
- No training on customer data
- Entra ID with RBAC
- Audit logging
- Prepared for municipal risk analysis (ROS)

## ✅ Key features

- Automated invoice data extraction
- AI-assisted accounting classification
- Human approval workflow
- Secure, auditable, and scalable architecture
