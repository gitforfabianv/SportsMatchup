#!/bin/bash

# Exit on any error
set -e

echo "Updating package index..."
sudo apt update

echo "Installing Node.js and npm..."
sudo apt install -y nodejs npm

echo "Installing Python3-pip..."
sudo apt install -y python3 python3.13-venv

echo "Verifying installation..."
node -v
npm -v

echo "npm and Node.js have been successfully installed!"

