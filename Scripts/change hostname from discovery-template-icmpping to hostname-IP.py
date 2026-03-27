import csv
import requests
import re

ZABBIX_URL = "http://192.168.0.165:8080/api_jsonrpc.php"
API_TOKEN = "97065c4bc5bbf3a543496e151cc25f72e2dd8fdfbf0f58ab3c788f58098f3c9e"
ICMP_TEMPLATE_NAME = "ICMP Ping"
CSV_FILE = "Book1.csv"     # file bạn convert từ Excel



headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}

# --- 1. Load CSV → tạo map IP → Hostname ---
mapping = {}
with open(CSV_FILE, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ip = row["IP"].strip()
        hostname = row["Hostname"].strip()
        mapping[ip] = hostname

print("[INFO] Mapping loaded:", len(mapping), "entries")

# --- 2. Lấy template ID ---
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

print(f"[INFO] Template ID = {template_id}")

# --- 3. Lấy host dùng ICMP Ping ---
payload_hosts = {
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": ["hostid", "host"],
        "selectInterfaces": ["ip"],
        "templateids": template_id
    },
    "id": 2
}

hosts_res = requests.post(ZABBIX_URL, headers=headers, json=payload_hosts).json()

ip_regex = re.compile(r"\b\d{1,3}(\.\d{1,3}){3}\b")

# --- 4. Rename theo logic ---
for h in hosts_res["result"]:
    hostid = h["hostid"]
    hostname = h["host"]       # có thể là IP hoặc tên AP
    ip = h["interfaces"][0]["ip"]

    # Logic quan trọng:
    # Nếu hostname == IP → host auto-add → cần rename
    if hostname == ip:
        if ip not in mapping:
            print(f"[WARN] IP {ip} không có trong mapping → skip")
            continue

        new_hostname = mapping[ip]
        new_visible  = f"{new_hostname} {ip}"

        payload_update = {
            "jsonrpc": "2.0",
            "method": "host.update",
            "params": {
                "hostid": hostid,
                "host": new_hostname,  # đổi hostname
                "name": new_visible    # đổi visible name
            },
            "id": 3
        }

        requests.post(ZABBIX_URL, headers=headers, json=payload_update)

        print(f"[UPDATED] {hostname} → {new_visible}")

    else:
        # Host đã rename → không sửa
        print(f"[SKIP] already named: {hostname}")

print("DONE.")