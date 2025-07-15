# deploy.sh

#!/bin/bash

set -e

# Ensure Docker is installed
if ! command -v docker &> /dev/null; then
  echo "Docker not found. Please install Docker."
  exit 1
fi

# Prepare acme.json for Traefik SSL certificates
echo "🔐 Setting up acme.json for Traefik..."
touch traefik/acme.json
chmod 600 traefik/acme.json

# Pull base images
echo "📥 Pulling base Docker images..."
docker pull mariadb:10.6
docker pull redis:alpine

echo "📦 Building ERPNext and Django images locally..."
#cd erpnext
#cp .env-example .env 2>/dev/null || true
#cd ..
docker compose build

# Launch all containers
echo "🚀 Starting services..."
docker compose up -d

# Wait a moment
sleep 10

echo "✅ Deployment complete!"
echo "➡️ Visit: https://provision.yourdomain.com to register your first company"
echo "🌐 Then open: https://yourcompany-erp.yourdomain.com"
