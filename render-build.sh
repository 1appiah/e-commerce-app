#!/usr/bin/env bash
# Install system dependencies
sudo apt-get update && sudo apt-get install -y wkhtmltopdf

# Install Python dependencies
pip install -r requirements.txt
