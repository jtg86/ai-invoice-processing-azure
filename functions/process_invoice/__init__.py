import json
import logging
import os
from typing import Any, Dict

import azure.functions as func
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

FORM_RECOGNIZER_ENDPOINT = os.environ["FORM_RECOGNIZER_ENDPOINT"]
FORM_RECOGNIZER_KEY = os.environ["FORM_RECOGNIZER_KEY"]


def _field_value(fields: Dict[str, Any], name: str, default: Any = None) -> Any:
    field = fields.get(name)
    if not field:
        return default
    return field.value


def main(blob: func.InputStream) -> str:
    logging.info("Processing invoice blob: %s", blob.name)

    client = DocumentAnalysisClient(
        endpoint=FORM_RECOGNIZER_ENDPOINT,
        credential=AzureKeyCredential(FORM_RECOGNIZER_KEY),
    )

    poller = client.begin_analyze_document(
        model_id="prebuilt-invoice",
        document=blob.read(),
    )

    result = poller.result()
    invoice = result.documents[0].fields if result.documents else {}

    total = _field_value(invoice, "InvoiceTotal")

    parsed = {
        "supplier": _field_value(invoice, "VendorName"),
        "invoiceNumber": _field_value(invoice, "InvoiceId"),
        "invoiceDate": str(_field_value(invoice, "InvoiceDate")),
        "totalAmount": getattr(total, "amount", None),
        "currency": getattr(total, "currency", None),
        "confidence": result.confidence,
    }

    return json.dumps(parsed, indent=2, ensure_ascii=False)
