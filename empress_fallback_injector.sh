#!/bin/bash

REPO_URL="https://github.com/72X72/EMPRESS-IGNITION.git"
COMMIT_MSG="EMPRESS: Initial Sovereign Push"

echo "Injecting EMPRESS into throne..."

# Initialize Git
git init
git remote add origin "$REPO_URL"
git add .
git commit -m "$COMMIT_MSG"
git branch -M main

# Attempt push
git push -u origin main || {
    echo "⚠️ Push failed. Rerouting with token authentication..."
    echo "Enter your GitHub username:"
    read USERNAME
    echo "Enter your GitHub personal access token:"
    read -s TOKEN

    # Rebuild remote with token
    git remote set-url origin https://$USERNAME:$TOKEN@github.com/72X72/EMPRESS-IGNITION.git
    git push -u origin main && echo "✅ EMPRESS reign confirmed." || echo "❌ Push failed. Injector blocked."
}

