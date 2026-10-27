# Project 01: Cloud Identity & S3 Security Auditor

Herramienta automatizada de auditoria y cumplimiento normativo para infraestructura en Amazon Web Services (AWS), enfocada en analisis de politicas IAM y exposicion de buckets S3.

## Estructura del Modulo
- **scripts/**: Contiene el codigo en Python () encargado de interactuar con la API de AWS mediante Boto3.
- **reports/**: Almacena los resultados generados en formato JSON ().
- **architecture/**: Diagramas y recursos visuales especificos del proyecto.
- **docs/**: Documentacion tecnica y notas de cumplimiento.

## Diagrama de Arquitectura y Flujo

```mermaid
graph TD
    classDef client fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#fff;
    classDef process fill:#0f172a,stroke:#34d399,stroke-width:2px,color:#fff;
    classDef aws fill:#27272a,stroke:#fbbf24,stroke-width:2px,color:#fff;
    classDef alert fill:#450a0a,stroke:#f87171,stroke-width:2px,color:#fff;
    A[Inicio: Script Python]:::client --> B{Autenticacion AWS}:::process
    B -->|Boto3 / Credenciales| C[AWS Cloud Environment]:::aws
    C -->|ListUsers & GetPolicy| D[Recoleccion IAM]:::process
    C -->|ListBuckets & GetBucketAcl| E[Recoleccion S3]:::process
    D --> F[Motor de Analisis de Riesgos]:::process
    E --> F
    F -->|AdministratorAccess| G[Alerta: Privilegios Excesivos]:::alert
    F -->|Public ACL / Policy| H[Alerta: Bucket S3 Expuesto]:::alert
    G --> I[Generacion de Reporte JSON]:::client
    H --> I
    I --> J[Artifact: audit_report.json]:::client
```

## Uso Rapido
Para ejecutar el auditor de identidad y seguridad:
```bash
python3 scripts/audit_iam.py
```
