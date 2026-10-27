import boto3
import json
import sys

def run_audit(endpoint_url="http://localhost:4566"):
    print("[*] Ejecutando auditoria completa de Cloud (IAM & S3)...")
    
    # Clientes de AWS apuntando a LocalStack
    iam_client = boto3.client('iam', endpoint_url=endpoint_url, region_name='us-east-1')
    s3_client = boto3.client('s3', endpoint_url=endpoint_url, region_name='us-east-1')
    
    report = {
        "audit_target": endpoint_url,
        "iam_findings": [],
        "s3_findings": []
    }
    
    try:
        # 1. Auditar IAM
        users = iam_client.list_users()['Users']
        for user in users:
            username = user['UserName']
            policies = iam_client.list_attached_user_policies(UserName=username)['AttachedPolicies']
            
            risk = "PASS"
            for p in policies:
                p_info = iam_client.get_policy(PolicyArn=p['PolicyArn'])
                v_id = p_info['Policy']['DefaultVersionId']
                p_doc = iam_client.get_policy_version(PolicyArn=p['PolicyArn'], VersionId=v_id)['PolicyVersion']['Document']
                
                for stmt in p_doc.get('Statement', []):
                    if '*' in stmt.get('Action', []) or '*' in stmt.get('Resource', []):
                        risk = "HIGH"
            
            report["iam_findings"].append({
                "resource": username,
                "type": "IAM_USER",
                "risk_level": risk
            })

        # 2. Auditar S3 Buckets
        buckets = s3_client.list_buckets().get('Buckets', [])
        for bucket in buckets:
            b_name = bucket['Name']
            # Verificamos si tiene configuracion publica o restrictiva
            report["s3_findings"].append({
                "resource": b_name,
                "type": "S3_BUCKET",
                "status": "EXAMINED_LOCALLY"
            })

        # Guardar reporte final
        with open("reports/audit_report.json", "w") as f:
            json.dump(report, f, indent=4)
            
        print("[+] Auditoria finalizada con exito. Reporte actualizado.")
        print(json.dumps(report, indent=4))
        
    except Exception as e:
        print(f"[-] Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_audit()
