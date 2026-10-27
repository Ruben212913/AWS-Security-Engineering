import subprocess
import sys
import os

GITHUB_USER = "Ruben212913"
REPO_NAME = "AWS-Security-Engineering"

def run_command(command, allow_failure=False):
    print(f"[*] Ejecutando: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        if allow_failure:
            print(f"[-] Aviso (continuando): {result.stderr.strip()}")
            return
        print(f"[-] Error: {result.stderr.strip()}")
        sys.exit(1)
    print(f"[+] Éxito: {result.stdout.strip()}")

def main():
    # Obtener el token de forma segura desde las variables de entorno de la terminal
    github_token = os.environ.get("GH_TOKEN")
    if not github_token:
        print("[-] Error: La variable de entorno GH_TOKEN no está configurada.")
        print("    Ejecuta: export GH_TOKEN='tu_token_aqui'")
        sys.exit(1)

    commit_msg = sys.argv[1] if len(sys.argv) > 1 else "feat: update AWS security engineering portfolio"
    
    print("--- INICIANDO AUTOMATIZACIÓN DE GIT: AWS-SECURITY-ENGINEERING ---")
    
    # 1. Configurar la URL remota inyectando el token de manera segura solo en memoria
    remote_url = f"https://{github_token}@github.com/{GITHUB_USER}/{REPO_NAME}.git"
    run_command(f"git remote set-url origin {remote_url}")
    
    # 2. Agregar cambios
    run_command("git add .")
    
    # 3. Hacer commit del cambio limpio
    run_command(f'git commit -m "{commit_msg}"', allow_failure=True)
    
    # 4. Empujar los cambios a GitHub
    run_command("git push -u origin main")
    
    print("[+] ¡Proyecto sincronizado y subido a AWS-Security-Engineering con éxito y seguridad!")

if __name__ == "__main__":
    main()
