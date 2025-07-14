#!/bin/bash

set -e

if ! command -v docker &> /dev/null; then
  echo "Docker not found. Please install Docker."
  exit 1
fi

echo "🔐 Creating acme.json..."
touch traefik/acme.json
chmod 600 traefik/acme.json

echo "📦 Pulling and building Docker containers..."
docker compose pull

echo "🚀 Starting all containers..."
docker compose up -d --build

sleep 10

echo "✅ Deployment complete!"
echo "Visit: https://provision.yourdomain.com"
