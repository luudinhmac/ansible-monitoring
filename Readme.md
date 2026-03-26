# 🚀 Zabbix 7.0 & Grafana Automation Stack

Dự án này thực hiện tự động hóa hoàn toàn quy trình triển khai hệ thống giám sát (Monitoring) trên nền tảng **Ubuntu 24.04 LTS**. Hệ thống được thiết kế tối ưu cho hạ tầng mạng và hệ thống tại **SPC**, đảm bảo tính bảo mật và hiệu suất cao.

---

## 📋 Mục lục
1. [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
2. [Cài đặt môi trường](#-cài-đặt-môi-trường)
3. [Cấu hình SSH & Bảo mật](#-cấu-hình-ssh--bảo-mật)
4. [Cấu trúc dự án](#-cấu-trúc-dự-án)
5. [Quy trình triển khai (Deployment)](#-quy-trình-triển-khai)
6. [Dọn dẹp hệ thống (Cleanup)](#-dọn-dẹp-hệ-thống)

---

## 💻 Yêu cầu hệ thống
* **Hệ điều hành:** Ubuntu 24.04 LTS (Noble Numbat).
* **Ansible:** Phiên bản 2.10 trở lên.
* **Tài khoản:** User có quyền `sudo` (Ví dụ: `macld`).

---

## 🛠 Cài đặt môi trường
Chạy các lệnh sau trên máy điều khiển (**Control Node**) để cài đặt Ansible:

```bash
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible -y
```

## 🔑 Cấu hình SSH & Bảo mật
### 1. Thiết lập SSH Key (Truy cập không mật khẩu)
Khởi tạo và đẩy SSH Key tới máy đích (192.168.157.133):

#### Tạo Key (tên mặc định id_ed25519)
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519

#### Copy Key sang Server đích
ssh-copy-id -i ~/.ssh/id_ed25519.pub macld@192.168.157.133
### 2. Quản lý bí mật với Ansible Vault
Dự án sử dụng Ansible Vault để bảo vệ mật khẩu Database và thông tin nhạy cảm.

#### Tạo file biến mã hóa
ansible-vault create group_vars/all.yml
Nội dung biến cần định nghĩa:

```bash
zabbix_db_pass: "MacLD_Secure_2026"
zabbix_version: "7.0"
timezone: "Asia/Ho_Chi_Minh"
server_ip: "192.168.157.133"
```
## 📂 Cấu trúc dự án
Tổ chức thư mục dự án theo tiêu chuẩn Role-based:

```Bash
mkdir -p ~/ansible-monitoring/group_vars
mkdir -p ~/ansible-monitoring/roles/{mariadb,zabbix_server,grafana}/{tasks,templates,handlers}
cd ~/ansible-monitoring
```

Sơ đồ thư mục:
Plaintext
~/ansible-monitoring/
├── site.yml                # Playbook thực thi cài đặt chính
├── cleanup.yml             # Playbook xóa trắng tài nguyên (Reset Lab)
├── inventory.ini           # Quản lý danh sách IP Server
├── group_vars/
│   └── all.yml             # Biến hệ thống (Mã hóa bởi Vault)
└── roles/
    ├── mariadb/            # Tự động cài đặt & Cấu hình MariaDB
    ├── zabbix_server/      # Tự động cài đặt Zabbix, Nginx & PHP 8.3
    └── grafana/            # Tự động cài đặt Grafana Dashboard

### 🚀 Quy trình triển khai
Bước 1: Khởi chạy Playbook
Thực hiện lệnh sau để bắt đầu quá trình cài đặt tự động:

```bash
ansible-playbook site.yml --ask-vault-pass -K
```
Bước 2: Kiểm tra kết quả
Zabbix Web UI: http://192.168.157.133

Tài khoản: Admin

Mật khẩu: zabbix (Nhớ đổi ngay sau khi đăng nhập).

Grafana UI: http://192.168.157.133:3000

Tài khoản: admin
Mật khẩu: admin

Tính năng đặc biệt: Dự án đã tích hợp Automation để tự động tạo file zabbix.conf.php, giúp bỏ qua các bước Setup Wizard thủ công trên trình duyệt.

## 🧹 Dọn dẹp hệ thống
Trong trường hợp cần xóa sạch cấu hình, Package và Database để làm lại từ đầu:

```Bash
ansible-playbook cleanup.yml --ask-vault-pass -K
```
Cảnh báo: Lệnh này sẽ yêu cầu bạn xác nhận bằng cách gõ yes. Khi thực hiện, toàn bộ dữ liệu giám sát sẽ bị xóa vĩnh viễn.

🛡 Bảo mật Git
Dự án được cấu hình để không upload file group_vars/all.yml lên GitHub. Hãy đảm bảo file .gitignore của bạn có nội dung sau:
```bash
group_vars/all.yml
.vault_pass.txt
*.retry
```

# Tác giả: Lưu Đình Mác
