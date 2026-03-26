🚀 Zabbix 7.0 & Grafana Automation Stack
Dự án sử dụng Ansible để tự động hóa hoàn toàn quy trình triển khai hệ thống giám sát (Monitoring) trên nền tảng Ubuntu 24.04 LTS. Hệ thống bao gồm Zabbix Server, MariaDB, Nginx, PHP 8.3 và Grafana Dashboard.

📋 Mục lục
Yêu cầu hệ thống

Cài đặt môi trường

Cấu hình SSH & Bảo mật

Cấu trúc dự án

Triển khai (Deployment)

Dọn dẹp (Cleanup)

💻 Yêu cầu hệ thống
OS: Ubuntu 24.04 (Noble Numbat)

Ansible: Phiên bản 2.10 trở lên

Quyền hạn: User có khả năng sudo (Ví dụ: macld)

🛠 Cài đặt môi trường
Chạy các lệnh sau trên máy điều khiển (Control Node) để cài đặt Ansible:

Bash
sudo apt update && sudo apt install software-properties-common -y
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible -y
🔑 Cấu hình SSH & Bảo mật
1. Thiết lập SSH Key (Passwordless)
Để Ansible có thể điều khiển máy đích (192.168.157.133) mà không cần nhập pass SSH:

Bash
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519
ssh-copy-id -i ~/.ssh/id_ed25519.pub macld@192.168.157.133
2. Quản lý bí mật với Ansible Vault
Dự án sử dụng Vault để mã hóa các thông tin nhạy cảm. Tạo file biến:

Bash
ansible-vault create group_vars/all.yml
Nội dung file (Sau khi giải mã):

YAML
zabbix_db_pass: "MacLD_Secure_2026"
server_ip: "192.168.157.133"
timezone: "Asia/Ho_Chi_Minh"
📂 Cấu trúc dự án
Dự án được tổ chức theo mô hình Role-based, giúp dễ dàng mở rộng và bảo trì:

Plaintext
~/ansible-monitoring/
├── site.yml            # Playbook chính để cài đặt
├── cleanup.yml         # Playbook để xóa sạch hệ thống
├── inventory.ini       # Khai báo IP Server đích
├── group_vars/         # Chứa biến (Đã được mã hóa Vault)
└── roles/              # Các vai trò (Common, MariaDB, Zabbix, Grafana)
🚀 Triển khai (Deployment)
Để bắt đầu cài đặt toàn bộ Stack giám sát, chạy lệnh sau:

Bash
ansible-playbook site.yml --ask-vault-pass -K
--ask-vault-pass: Nhập mật khẩu để mở file all.yml.

-K: Nhập mật khẩu sudo của máy đích.

Sau khi hoàn tất:

Zabbix Web: http://192.168.157.133 (User: Admin / Pass: zabbix)

Grafana: http://192.168.157.133:3000 (User: admin / Pass: admin)

🧹 Dọn dẹp (Cleanup)
Nếu muốn xóa sạch toàn bộ cấu hình, Package và Database để làm lại từ đầu:

Bash
ansible-playbook cleanup.yml --ask-vault-pass -K
Lưu ý: Lệnh này có tích hợp bước xác nhận (Confirmation) để tránh xóa nhầm.

Duy trì bởi: Lưu Đình Mác
