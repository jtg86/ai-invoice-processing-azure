# Security & GDPR

This portfolio project is designed to show how an AI-based invoice processing solution can align with GDPR and public sector requirements.

## Data protection principles

- **Data residency:** All data is stored and processed in **Norway East**.
- **No training on customer data:** AI services are configured so customer data is not used for training.
- **Encryption:** Data is encrypted at rest and in transit using Azure-managed keys.
- **Access control:** Authentication and authorization are enforced with **Entra ID** and Azure RBAC.

## Traceability & logging

- **Application Insights** captures structured logs and performance metrics.
- **Audit trail** is preserved for each invoice (upload, extraction, approval, final disposition).
- **Correlation IDs** can be added for end-to-end tracking.

## Human-in-the-loop

- AI results are **reviewed and approved** before posting to an ERP system.
- Manual overrides and rejection flows are supported via Power Apps or custom UI.

## Compliance readiness

- Designed for **GDPR**, **public sector**, and **municipal** contexts.
- Ready for **risk and vulnerability assessment (ROS)**.

> This repository is a demonstration only and not production-ready.
