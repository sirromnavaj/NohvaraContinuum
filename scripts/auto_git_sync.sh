#!/bin/bash

# Navigate to the project directory
cd "$HOME/NohvaraContinuum" || exit

# Check for changes
if [[ -n $(git status --porcelain) ]]; then
    # Stage all changes
    git add --all

    # Commit changes with timestamp
    git commit -m "Auto-sync: $(date +'%Y-%m-%d %H:%M:%S')"

    # Pull latest changes to avoid conflicts
    git pull --rebase origin main

    # Push changes to GitHub
    git push origin main
fi
