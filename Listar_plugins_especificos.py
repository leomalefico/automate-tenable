import json
import requests

url = "https://cloud.tenable.com/workbenches/vulnerabilities"
severity_mapping = {4: "Critical", 3: "High", 2: "Medium", 1: "Low", 0: "Info"}

with open("api_keys.json") as f:
    client_api_keys = json.load(f)

plugin_ids_input = input("Digite os IDs dos plugins desejados separados por vírgula: ")
plugin_ids = [int(id.strip()) for id in plugin_ids_input.split(",")]

for client, api_keys in client_api_keys.items():
    headers = {
        "accept": "application/json",
        "X-ApiKeys": f"accessKey={api_keys['accessKey']};secretKey={api_keys['secretKey']}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()

        print(f"Cliente: {client}\n")

        plugin_found = False  
        
        for vulnerability in data["vulnerabilities"]:
            severity = vulnerability["severity"]
            plugin_id = vulnerability["plugin_id"]

            if plugin_id in plugin_ids:
                count = vulnerability['count']
                plugin_name = vulnerability["plugin_name"]
                vulnerability_state = vulnerability["vulnerability_state"]
                cvss3_base_score = vulnerability['cvss3_base_score']

                severity_text = severity_mapping.get(severity, "Unknown")

                print(f"Plugin ID: {plugin_id}")
                print(f"Plugin Name: {plugin_name}")
                print(f"Vulnerability State: {vulnerability_state}")
                print(f"Severity: {severity_text}")
                print(f"CVSS3 Base Score: {cvss3_base_score}")
                print(f"Count: {count}")
                print("-" * 25)
                
                plugin_found = True  

        if not plugin_found:
            print("Não foi encontrado nenhum ativo com esta vulnerabilidade")

        print("\n" + "#" * 50 + "\n")  
    else:
        print(f"Failed to retrieve data for client {client}")
