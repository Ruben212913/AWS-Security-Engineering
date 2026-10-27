# Project 01: Cloud Identity & S3 Security Auditor

Automated auditing and compliance tool for Amazon Web Services (AWS) infrastructure, focusing on IAM policy analysis and S3 bucket exposure detection.

## Module Structure
- **scripts/**: Contains the core Python script () interacting with the AWS API via Boto3.
- **reports/**: Stores generated security findings in JSON format ().
- **architecture/**: Project-specific visual diagrams and assets.
- **docs/**: Technical documentation and compliance notes.

## Architecture & Audit Flow Diagram

```mermaid
graph TD
    classDef client fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#fff;
    classDef process fill:#0f172a,stroke:#34d399,stroke-width:2px,color:#fff;
    classDef aws fill:#27272a,stroke:#fbbf24,stroke-width:2px,color:#fff;
    classDef alert fill:#450a0a,stroke:#f87171,stroke-width:2px,color:#fff;
    A[Start: Python Script]:::client --> B{AWS Authentication}:::process
    B -->|Boto3 / Credentials| C[AWS Cloud Environment]:::aws
    C -->|ListUsers & GetPolicy| D[IAM Data Collection]:::process
    C -->|ListBuckets & GetBucketAcl| E[S3 Data Collection]:::process
    D --> F[Risk Analysis Engine]:::process
    E --> F
    F -->|AdministratorAccess| G[Alert: Excessive Privileges]:::alert
    F -->|Public ACL / Policy| H[Alert: Exposed S3 Bucket]:::alert
    G --> I[JSON Report Generation]:::client
    H --> I
    I --> J[Artifact: audit_report.json]:::client
```

## Quickstart
To execute the identity and security auditor:
```bash
python3 scripts/audit_iam.py
```
