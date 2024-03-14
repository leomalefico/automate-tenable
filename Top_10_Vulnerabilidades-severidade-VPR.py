import json
from tenable.io import TenableIO

# Carregar chaves da API a partir de um arquivo JSON
with open("api_keys.json", "r") as f:
    api_keys = json.load(f)

# Mapeamento de severidade para texto descritivo
severity_mapping = {4: "Critical", 3: "High", 2: "Medium", 1: "Low", 0: "Info"}

# Iterar sobre os clientes e suas chaves API
for client, keys in api_keys.items():
    print(f"Client: {client}")
    
    # Obter as chaves de acesso
    access_key = keys['accessKey']
    secret_key = keys['secretKey']
    
    # Criar uma instância da TenableIO com as chaves de acesso
    tio = TenableIO(access_key=access_key, secret_key=secret_key)

    # Recuperar vulnerabilidades usando o método `vulns` do objeto WorkbenchesAPI
    vulnerabilities = tio.workbenches.vulns()
    
    # Filtrar e classificar as vulnerabilidades
    sorted_vulnerabilities = []
    for vuln in vulnerabilities:
        # Filtro para qual severidade deseja listar
        if vuln["severity"] >= 4:  
            vpr_score = vuln.get('vpr_score', None)
            # Filtro para identificar qual score deseja listar
            if vpr_score is not None and vpr_score >= 10:  
                sorted_vulnerabilities.append(vuln)
                
    # Ordenar as vulnerabilidades por contagem
    sorted_vulnerabilities = sorted(sorted_vulnerabilities, key=lambda x: x["count"], reverse=True)
    
    # Verificar se há vulnerabilidades para exibir
    if not sorted_vulnerabilities:
        print("Não foram encontradas vulnerabilidades ativas para este VPR / Severidade")
        print("\n")
    else:
        print("Top 10 Vulnerabilities:")
        # Exibir as 10 principais vulnerabilidades
        for idx, vulnerability in enumerate(sorted_vulnerabilities[:10], 1):
            severity_text = severity_mapping.get(vulnerability["severity"], "Unknown")
            print(f"Plugin ID: {vulnerability['plugin_id']}, Plugin Name: {vulnerability['plugin_name']}, Vulnerability State: {vulnerability['vulnerability_state']}, Severity: {severity_text}, VPR Score: {vulnerability.get('vpr_score', 'N/A')}, Count: {vulnerability['count']}")
        print("\n")
