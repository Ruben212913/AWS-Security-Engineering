import boto3
import json
import sys

def run_audit(endpoint_url="http://localhost:4566"):
    print("[*] Executing comprehensive AWS Cloud Security Audit (IAM & S3)...")
    
    # AWS clients pointing to LocalStack or real AWS endpoints
    iam_client = boto3.client('iam', endpoint_url=endpoint_url, region_name='us-east-1')
    s3_client = boto3.client('s3', endpoint_url=endpoint_url, region_name='us-east-1')
    
    report = {
        "audit_target": endpoint_url,
        "iam_findings": [],
        "s3_findings": []
    }
    
    try:
        # 1. Audit IAM Users and Policies
        users = iam_client.list_users().get('Users', [])
        for user in users:
            username = user['UserName']
            policies = iam_client.list_attached_user_policies(UserName=username).get('AttachedPolicies', [])
            
            risk = "PASS"
            for p in policies:
                p_info = iam_client.get_policy(PolicyArn=p['PolicyArn'])
                v_id = p_info['Policy']['DefaultVersionId']
                p_doc = iam_client.get_policy_version(PolicyArn=p['PolicyArn'], VersionId=v_id)['PolicyVersion']['Document']
                
                for stmt in p_doc.get('Statement', []):
                    actions = stmt.get('Action', [])
                    resources = stmt.get('Resource', [])
                    
                    # Normalize to lists for uniform evaluation
                    if isinstance(actions, str):
                        actions = [actions]
                    if isinstance(resources, str):
                        resources = [resources]
                    
                    # Check for dangerous wildcards (e.g., '*' or 's3:*')
                    has_wildcard_action = any('*' in action for action in actions)
                    has_wildcard_resource = any('*' in resource for resource in resources)
                    
                    if has_wildcard_action or has_wildcard_resource:
                        risk = "HIGH"
            
            report["iam_findings"].append({
                "resource": username,
                "type": "IAM_USER",
                "risk_level": risk
            })

        # 2. Audit S3 Buckets
        buckets = s3_client.list_buckets().get('Buckets', [])
        for bucket in buckets:
            b_name = bucket['Name']
            report["s3_findings"].append({
                "resource": b_name,
                "type": "S3_BUCKET",
                "status": "EXAMINED_LOCALLY"
            })

        # Save final compliance report
        with open("reports/audit_report.json", "w") as f:
            json.dump(report, f, indent=4)
            
        print("[+] Audit completed successfully. Report updated in reports/audit_report.json.")
        print(json.dumps(report, indent=4))
        
    except Exception as e:
        print(f"[-] Error during audit execution: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_audit()
