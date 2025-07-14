# README.md

## 🚀 ERPNext SaaS Starter

This project is a production-ready ERP SaaS starter kit built with **ERPNext**, **Django**, **Docker**, and **Traefik** to enable multi-tenant ERP instances on a single server. Each company can register via a UI and get their own ERPNext site with a custom subdomain — all automated.

---

## 🧱 Tech Stack
- [ERPNext v15](https://erpnext.com/)
- [Frappe Framework](https://frappeframework.com/)
- Django (Provisioning API + UI)
- Docker & Docker Compose
- Traefik 2 (Reverse Proxy + Auto HTTPS)

---

## 🌐 Subdomain Routing
- ERP Sites: `company1.preciseerp.com`, `company2.preciseerp.com`
- Django Admin: `provision.preciseerp.com`

Traefik handles SSL & routing automatically via Let's Encrypt.

---

## 📁 Folder Structure
```
erp_saas/
├── docker-compose.yml
├── traefik/                 # Traefik reverse proxy config
│   └── traefik.yml
├── envs/                    # Environment variables
├── django/                  # Django provisioning UI/API
├── deploy.sh                # Deployment automation script
└── erpnext/                 # frappe_docker (added as submodule or clone)
```

---

## ⚙️ Setup Instructions

### 1. 🚀 Clone the Repo
```bash
git clone https://github.com/yourname/erp_saas.git
cd erp_saas
```

### 2. ➕ Add frappe_docker
```bash
git submodule add https://github.com/frappe/frappe_docker.git erpnext
cd erpnext
git checkout version-15
cd ..
```

Alternatively, clone manually:
```bash
git clone -b version-15 https://github.com/frappe/frappe_docker.git erpnext
```

### 3. 🔐 Setup DNS
In your DNS provider:
- Add wildcard A record for `*.preciseerp.com` → server IP
- Add A record for `provision.preciseerp.com` → server IP

### 4. 📜 Prepare & Run Deploy Script
```bash
chmod +x deploy.sh
./deploy.sh
```

### 5. 🛠 Replace Placeholders
Edit `docker-compose.yml` and `traefik.yml`, replace:
- `preciseerp.com`
- `your-email@example.com`

---

## 🏢 Register a Company
Visit: `https://provision.preciseerp.com`
- Fill out company name + subdomain
- Django will call Frappe to run `bench new-site` + `install-app erpnext`
- Visit `https://subdomain.preciseerp.com` to access ERP

---

## 🧪 Testing Locally (Optional)
Use a local DNS resolver or edit `/etc/hosts` for `*.localhost`

---

## 📦 Backup & Maintenance
- Backup MariaDB volume `mariadb-data`
- Backup site volume `sites-vol`
- Monitor logs with `docker logs -f <container>`

---

## 📄 License
MIT (for this orchestration)
ERPNext & Frappe are under GPLv3

---

## 🙋‍♂️ Questions?
Feel free to raise an issue or contact [your-email@example.com].

---

## 🛠️ deploy.sh (auto-setup script)
```bash
#!/bin/bash

set -e

# Ensure Docker is installed
if ! command -v docker &> /dev/null; then
  echo "Docker not found. Please install Docker."
  exit 1
fi

# Prepare acme.json
echo "🔐 Creating acme.json..."
touch traefik/acme.json
chmod 600 traefik/acme.json

# Pull images and build
echo "📦 Pulling and building Docker containers..."
docker compose pull

echo "🚀 Starting all containers..."
docker compose up -d --build

# Wait for services
sleep 10

echo "✅ Deployment complete!"
echo "Visit: https://provision.preciseerp.com"
```
