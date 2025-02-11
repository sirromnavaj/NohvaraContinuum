#!/bin/bash

LOG_FILE="../logs/optimization.log"
ARCHIVE_DIR="../logs/archives"
BACKUP_DIR="../backups"
AI_DATA_DIR="../ai_engine"
SYSTEM_CONFIGS="../config"
DATE=$(date '+%Y-%m-%d_%H-%M-%S')
EMAIL="morrisandanje@gmail.com"

# Function to log messages and send email alerts
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
    
    # If the message is critical, send an email alert
    if [[ "$1" == *"Critical"* || "$1" == *"Restoring from latest backup"* ]]; then
        echo "$1" | mail -s "⚠ Nohvara Continuum System Alert" $EMAIL
    fi
}

log_message "Starting system optimization with backup and recovery..."

# 1. **Create Backup Before Any Changes**
log_message "Creating backup of AI data, logs, and configurations..."
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" "$AI_DATA_DIR" "$SYSTEM_CONFIGS" "../logs" 2>/dev/null
log_message "Backup completed: backup_$DATE.tar.gz"

# 2. **Archive Old Logs Instead of Deleting**
log_message "Archiving logs older than 7 days..."
mkdir -p $ARCHIVE_DIR
find ../logs/ -type f -name "*.log" -mtime +7 -exec gzip -c {} > $ARCHIVE_DIR/$(basename {}).gz \; -exec rm {} \;
log_message "Old logs archived."

# 3. **Preserve AI Learning Data but Clean Temporary Files**
log_message "Clearing non-essential cache files..."
find ~/.cache/ -type f -atime +10 -delete  
find /data/data/com.termux/cache/ -type f -atime +10 -delete
log_message "Cache cleared."

# 4. **Smart Memory Optimization (Protecting AI Data)**
log_message "Optimizing memory while preserving AI state..."
sync && echo 1 > /proc/sys/vm/drop_caches  
log_message "Memory optimization completed."

# 5. **Ensure AI Core Stays Active**
log_message "Checking AI Core status..."
if ! pgrep -f "ai_core.py" > /dev/null; then
    log_message "Critical: AI Core is not running! Restarting..."
    nohup python3 ../ai_engine/ai_core.py > ../logs/ai_core_restart.log 2>&1 &
    log_message "AI Core restarted."
else
    log_message "AI Core is running normally."
fi

# 6. **Check for Missing or Corrupted Files**
log_message "Checking system integrity..."
MISSING_FILES=()

if [ ! -f "$AI_DATA_DIR/ai_core.py" ]; then
    MISSING_FILES+=("ai_core.py")
fi

if [ ! -d "$SYSTEM_CONFIGS" ]; then
    MISSING_FILES+=("config directory")
fi

if [ ${#MISSING_FILES[@]} -ne 0 ]; then
    log_message "Critical: Missing files detected: ${MISSING_FILES[*]}. Restoring from latest backup..."
    
    # Find the latest backup
    LATEST_BACKUP=$(ls -t "$BACKUP_DIR" | head -n 1)
    
    if [ -n "$LATEST_BACKUP" ]; then
        tar -xzf "$BACKUP_DIR/$LATEST_BACKUP" -C "../"
        log_message "Restoration completed using backup: $LATEST_BACKUP"
    else
        log_message "Critical: No backup found! Manual recovery may be needed."
    fi
else
    log_message "All essential files are intact."
fi

# 7. **Optimize Python Packages**
log_message "Checking for outdated Python packages..."
pip list --outdated > ../logs/pip_outdated.log
log_message "Updating outdated Python packages..."
pip install --upgrade $(awk '{print $1}' ../logs/pip_outdated.log | tail -n +3) 

# 8. **Disk Usage Monitoring**
DISK_USAGE=$(df -h | grep '/data')
log_message "Current Disk Usage: $DISK_USAGE"

log_message "System optimization and recovery completed successfully!"
exit 0
