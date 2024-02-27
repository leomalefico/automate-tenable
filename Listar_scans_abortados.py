import json
import requests

def load_api_keys(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def get_scans_data(api_key):
    url = "https://cloud.tenable.com/scans"
    headers = {
        "accept": "application/json",
        "X-ApiKeys": f"accessKey={api_key['accessKey']};secretKey={api_key['secretKey']}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        scans_data = response.json()["scans"]
        scans_aborted_found = False  
        for scan in scans_data:
            if scan["enabled"] == True:  
                scan_name = scan["name"]
                scan_status = scan["status"]
                if scan_status.lower() == "aborted":
                    print(f"Scan: {scan_name}, Status: {scan_status}")
                    scans_aborted_found = False
        if not scans_aborted_found:
            print("Não foram encontrados scans abortados na console")
    else:
        print("Erro ao obter os scans:", response.text)

    
def main():    
    api_keys = load_api_keys("api_keys.json")
    for client_name, key in api_keys.items():
        print("-------------------------------------------------")
        print(f"Scans VM abortados: Cliente '{client_name}':")
        get_scans_data(key)
        
if __name__ == "__main__":
    main()

       
    
    