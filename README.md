# AWS Security Engineering Portfolio

Repositorio especializado en arquitectura de seguridad, cumplimiento normativo y hardening de infraestructura en Amazon Web Services (AWS).

## Estructura del Repositorio
- **Project-01-Cloud-Identity-Auditor/**: Auditoría automatizada de políticas IAM, control de accesos y análisis de exposición de buckets S3 mediante scripts de Python orientados a cumplimiento normativo y estándares de seguridad.

## Diagrama de Arquitectura y Flujo de Auditoria

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
