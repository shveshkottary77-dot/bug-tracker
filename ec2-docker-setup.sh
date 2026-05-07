#!/bin/bash
# ─────────────────────────────────────────────────────────
# EC2 One-Time Docker Setup Script
# Run this ONCE on your EC2 instance after first launch.
# Usage: bash ec2-docker-setup.sh
# ─────────────────────────────────────────────────────────

set -e  # Exit immediately if any command fails

echo "🔄 Updating system packages..."
sudo apt update -y && sudo apt upgrade -y

echo "🐳 Installing Docker..."
sudo apt install -y docker.io

echo "⚙️  Enabling and starting Docker service..."
sudo systemctl enable docker
sudo systemctl start docker

echo "👤 Adding current user to docker group (no sudo needed)..."
sudo usermod -aG docker $USER

echo ""
echo "✅ Docker setup complete!"
echo ""
echo "Docker version:"
docker --version
echo ""
echo "⚠️  IMPORTANT: Log out and log back in for the docker group change to take effect."
echo "   Then you can verify with: docker ps"
