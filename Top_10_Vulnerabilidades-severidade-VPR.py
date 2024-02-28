import json
import os
import requests

with open("api_keys.json", "r") as f:
    api_keys = json.load(f)

url = "https://cloud.tenable.com/workbenches/vulnerabilities"
severity_mapping = {4: "Critical", 3: "High", 2: "Medium", 1: "Low", 0: "Info"}

for client, keys in api_keys.items():
    print(f"Client: {client}")

    headers = {
        "accept": "application/json",
        "X-ApiKeys": f"accessKey={keys['accessKey']};secretKey={keys['secretKey']}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        
        vulnerabilities = []  
        for vulnerability in data["vulnerabilities"]:
            severity = vulnerability["severity"]
            
            if severity == 4:  # Filtro para identificar qual severidade deseja listar
                
                count = vulnerability['count']
                plugin_id = vulnerability["plugin_id"]
                plugin_name = vulnerability["plugin_name"]
                vulnerability_state = vulnerability["vulnerability_state"]
                
                # Verifica se a chave 'vpr_score' está presente antes de acessá-la
                vpr_score = vulnerability.get('vpr_score', None)
                
                if vpr_score is not None and vpr_score >= 9.9: # Filtro para identificar qual score deseja listar
                    vulnerabilities.append({
                        "plugin_id": plugin_id,
                        "plugin_name": plugin_name,
                        "vulnerability_state": vulnerability_state,
                        "severity": severity,
                        "vpr_score": vpr_score,
                        "count": count
                    })

        # Ordenar a lista de vulnerabilidades com base no número de contagens (count)
        sorted_vulnerabilities = sorted(vulnerabilities, key=lambda x: x["count"], reverse=True)
        
        
        print("Top 10 Vulnerabilities:")
        for idx, vulnerability in enumerate(sorted_vulnerabilities[:10], 1):
            severity_text = severity_mapping.get(vulnerability["severity"], "Unknown")
            print(f"{idx}. Plugin ID: {vulnerability['plugin_id']}")
            print(f"   Plugin Name: {vulnerability['plugin_name']}")
            print(f"   Vulnerability State: {vulnerability['vulnerability_state']}")
            print(f"   Severity: {severity_text}")
            print(f"   VPR Score: {vulnerability.get('vpr_score', 'N/A')}")
            print(f"   Count: {vulnerability['count']}")
            print("-" * 50)
        print("\n")  
    else:
        print(f"Failed to fetch data for client: {client}. Status code: {response.status_code}")
