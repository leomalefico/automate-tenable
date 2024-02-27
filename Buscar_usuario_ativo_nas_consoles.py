import json
import requests

#################################################################
search_text = "leonar"  # NOME DO USUÁRIO (regra contains)
###################################### ###########################

def load_api_keys(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def get_users_data(api_key, search_text):
    url = "https://cloud.tenable.com/users"
    headers = {
        "accept": "application/json",
        "X-ApiKeys": f"accessKey={api_key['accessKey']};secretKey={api_key['secretKey']}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        users_data = response.json()["users"]
        found_user = False
        for user in users_data:
            if search_text.lower() in user["user_name"].lower():
                found_user = True
                print("Usuário:", user["user_name"])
                #print("uuid_id:", user["uuid_id"])
                print("Ativo:", user["enabled"])
        if not found_user:
            print("Não foi encontrado usuário com este nome")
            
    else:
        print(f"Failed to retrieve user data with API Key {api_key}. Status code:", response.status_code)



def main():    
    api_keys = load_api_keys("api_keys.json")
    for client_name, key in api_keys.items():
        print("-----------------------------")
        print(f"Cliente '{client_name}':")
        get_users_data(key, search_text)

if __name__ == "__main__":
    main()
