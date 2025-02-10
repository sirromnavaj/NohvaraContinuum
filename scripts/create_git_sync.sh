#!/bin/bash

# Define file path
SYNC_SCRIPT="$HOME/NohvaraContinuum/scripts/auto_git_sync.sh"

# Ensure the scripts directory exists
mkdir -p "$HOME/NohvaraContinuum/scripts"

# Create the auto git sync script
cat > "$SYNC_SCRIPT" << 'EOF'
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
EOF

# Make the script executable
chmod +x "$SYNC_SCRIPT"

# Confirm script creation
echo "✅ Git Sync Script Created: $SYNC_SCRIPT"
