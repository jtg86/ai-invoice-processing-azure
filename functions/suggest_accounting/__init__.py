import json
import logging
import os
from typing import Any, Dict

import azure.functions as func
import requests

OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
OPENAI_KEY = os.environ["AZURE_OPENAI_KEY"]
OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")


def _build_prompt(invoice: Dict[str, Any]) -> str:
    return (
        "You are an accounting assistant for a Norwegian municipality.\n\n"
        f"Invoice details:\n"
        f"Supplier: {invoice.get('supplier')}\n"
        f"Invoice number: {invoice.get('invoiceNumber')}\n"
        f"Invoice date: {invoice.get('invoiceDate')}\n"
        f"Total: {invoice.get('totalAmount')} {invoice.get('currency', 'NOK')}\n\n"
        "Suggest:\n- Account number\n- Cost center\n- Justification"
    )


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        payload = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON payload", status_code=400)

    prompt = _build_prompt(payload)

    body = {
        "messages": [
            {"role": "system", "content": "Return JSON only."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 200,
    }

    url = (
        f"{OPENAI_ENDPOINT}/openai/deployments/{OPENAI_DEPLOYMENT}/chat/completions"
        f"?api-version={OPENAI_API_VERSION}"
    )

    response = requests.post(
        url,
        headers={"api-key": OPENAI_KEY, "Content-Type": "application/json"},
        data=json.dumps(body),
        timeout=30,
    )

    if response.status_code >= 400:
        logging.error("OpenAI error: %s", response.text)
        return func.HttpResponse("OpenAI request failed", status_code=502)

    content = response.json()["choices"][0]["message"]["content"]
    return func.HttpResponse(content, status_code=200, mimetype="application/json")
