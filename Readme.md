1. Install ansible

sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible -y

2. Config SSH key to access via IP
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519
ssh-copy-id -i ~/.ssh/id_ed25519.pub username@192.168.157.133

3. Setting up directory structure project
mkdir -p ~/ansible-monitoring/group_vars
mkdir -p ~/ansible-monitoring/roles/{common,mariadb,zabbix_server,grafana}/{tasks,templates,handlers}
cd ~/ansible-monitoring

4. Using ansible-vault create group_vars/all.yml to protect password
ansible-vault create group_vars/all.yml

zabbix_db_pass: "MacLD_Secure_2026"
zabbix_version: "7.0"
timezone: "Asia/Ho_Chi_Minh"
server_ip: "192.168.157.133"


5. Run playbook
ansible-playbook site.yml --ask-vault-pass -K


6. Clean all resource
ansible-playbook cleanup.yml --ask-vault-pass -K
