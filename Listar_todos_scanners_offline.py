import json
import requests

def load_api_keys(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def get_scanners(api_key):
    url = "https://cloud.tenable.com/scanners"
    headers = {
        "accept": "application/json",
        "X-ApiKeys": f"accessKey={api_key['accessKey']};secretKey={api_key['secretKey']}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        offline_scanners_found = False  # Variável para verificar se foram encontrados scanners offline
        if "scanners" in data:
            scanners = data["scanners"]
            for scanner in scanners:
                name = scanner.get("name", "Nome não disponível")
                status = scanner.get("status", "Status não disponível")
                ip_addresses = scanner.get("ip_addresses", [])
                if name and status.lower() == "off" and ip_addresses:
                    print("Nome:", name)
                    print("Status:", f"{status} ( ( ( Warning ) ) )")
                    print("Endereços IP:")
                    for ip in ip_addresses:
                        print(ip)
                    print("")
                    offline_scanners_found = True  # Marcamos que encontramos scanners offline
        if not offline_scanners_found:
            print("Não há scanners offline.")
    else:
        print("Falha ao obter a lista de scanners. Código de status:", response.status_code)

def main():
    api_keys = load_api_keys("api_keys.json")

    
    for client_name, api_key in api_keys.items():
        print("-------------------------------------------")
        print(f"Scanners offline para o cliente '{client_name}':")
        get_scanners(api_key)

if __name__ == "__main__":
    main()
