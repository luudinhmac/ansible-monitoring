import requests

ZABBIX_URL = "http://192.168.0.165:8080/api_jsonrpc.php"
API_TOKEN = "97065c4bc5bbf3a543496e151cc25f72e2dd8fdfbf0f58ab3c788f58098f3c9e"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}

# Danh sách host muốn TEST trước
TEST_HOSTNAMES = [
    "APE44E.2D8A.1A48",
    "F1-MTC"
]

# Step 1: Lấy các host có trong danh sách cần test
payload = {
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": ["hostid", "host"],
        "selectInterfaces": ["ip"],
        "filter": {
            "host": TEST_HOSTNAMES
        }
    },
    "id": 1
}

response = requests.post(ZABBIX_URL, headers=headers, json=payload).json()

for h in response["result"]:
    hostid = h["hostid"]
    hostname = h["host"]
    ip = h["interfaces"][0]["ip"]

    new_visible_name = f"{hostname} {ip}"

    update_payload = {
        "jsonrpc": "2.0",
        "method": "host.update",
        "params": {
            "hostid": hostid,
            "name": new_visible_name
        },
        "id": 2
    }

    r = requests.post(ZABBIX_URL, headers=headers, json=update_payload).json()
    print(f"Updated {hostname} → {new_visible_name}")

print("TEST DONE")