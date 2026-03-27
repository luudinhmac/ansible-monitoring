import requests
import re

ZABBIX_URL = "http://192.168.0.165:8080/api_jsonrpc.php"
# User settings -> API tokens -> Create token
API_TOKEN = "97065c4bc5bbf3a543496e151cc25f72e2dd8fdfbf0f58ab3c788f58098f3c9e"
ICMP_TEMPLATE_NAME = "ICMP Ping"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}

# 1. Lấy template ID của "ICMP Ping"
payload_template = {
    "jsonrpc": "2.0",
    "method": "template.get",
    "params": {
        "output": ["templateid"],
        "filter": {"name": ICMP_TEMPLATE_NAME}
    },
    "id": 1
}

template_res = requests.post(ZABBIX_URL, headers=headers, json=payload_template).json()
template_id = template_res["result"][0]["templateid"]
print(f"[INFO] Template ICMP Ping ID = {template_id}")

# 2. Lấy danh sách host dùng template ICMP Ping
payload_hosts = {
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": ["hostid", "host", "name"],
        "selectInterfaces": ["ip"],
        "templateids": template_id
    },
    "id": 2
}

hosts_res = requests.post(ZABBIX_URL, headers=headers, json=payload_hosts).json()

# Regex kiểm tra Visible name đã chứa IP
ip_pattern = re.compile(r"\b\d{1,3}(\.\d{1,3}){3}\b")

for h in hosts_res["result"]:
    hostid = h["hostid"]
    hostname = h["host"]        # ap-14, apf3-201...
    visiblename = h["name"]     # Visible name hiện tại
    ip = h["interfaces"][0]["ip"]

    # nếu Visible name đã chứa IP → bỏ qua
    if ip_pattern.search(visiblename):
        print(f"SKIP: {visiblename}")
        continue

    # tạo visible name mới
    new_visible = f"{hostname} {ip}"

    # update visible name
    payload_update = {
        "jsonrpc": "2.0",
        "method": "host.update",
        "params": {
            "hostid": hostid,
            "name": new_visible
        },
        "id": 3
    }

    r = requests.post(ZABBIX_URL, headers=headers, json=payload_update).json()
    print(f"UPDATED: {hostname} → {new_visible}")

print("DONE!")