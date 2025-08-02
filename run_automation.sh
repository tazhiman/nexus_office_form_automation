#!/bin/bash

# Nexus Form Automation Runner Script
# Handles execution with proper logging and error handling

set -e

echo "🚀 Starting Nexus Form Automation Container"
echo "⏰ Container started at: $(date)"
echo "🌍 Timezone: $TZ"
echo "👤 Visitor: $VISITOR_NAME"
echo "🏢 Company: $COMPANY"
echo "============================================"

# Function to run automation
run_automation() {
    echo "📋 Executing form automation..."
    
    # Run the Python script and capture exit code
    if python3 /app/form_automation_lightweight.py; then
        echo "✅ Automation completed successfully at $(date)"
        echo "📄 Logs available in /app/logs/"
        return 0
    else
        echo "❌ Automation failed at $(date)"
        echo "📄 Check logs in /app/logs/ for details"
        return 1
    fi
}

# Function to wait for next execution (for cron mode)
wait_for_next_run() {
    local target_hour=6
    local target_minute=0
    
    while true; do
        current_hour=$(date +%H)
        current_minute=$(date +%M)
        
        # Calculate seconds until 6:00 AM
        if [ "$current_hour" -lt "$target_hour" ] || 
           ([ "$current_hour" -eq "$target_hour" ] && [ "$current_minute" -lt "$target_minute" ]); then
            # Today's 6:00 AM hasn't passed yet
            target_time="$target_hour:$target_minute"
        else
            # Wait for tomorrow's 6:00 AM
            target_time="$(date -d 'tomorrow' +%Y-%m-%d) $target_hour:$target_minute"
        fi
        
        seconds_to_wait=$(( $(date -d "$target_time" +%s) - $(date +%s) ))
        
        echo "⏳ Next execution scheduled for: $(date -d "$target_time")"
        echo "⏳ Waiting ${seconds_to_wait} seconds..."
        
        sleep $seconds_to_wait
        
        echo "⏰ Time for scheduled execution!"
        run_automation
        
        # Wait a bit to avoid running multiple times in the same minute
        sleep 60
    done
}

# Check execution mode
case "${EXECUTION_MODE:-once}" in
    "once")
        echo "🔄 Running in single execution mode"
        run_automation
        ;;
    "daily")
        echo "🔄 Running in daily scheduled mode (6:00 AM)"
        wait_for_next_run
        ;;
    "cron")
        echo "🔄 Running in cron mode"
        # Set up cron job for 6:00 AM daily
        echo "0 6 * * * cd /app && python3 form_automation_lightweight.py >> /app/logs/cron.log 2>&1" | crontab -
        echo "📅 Cron job scheduled for 6:00 AM daily"
        # Start cron service
        cron -f
        ;;
    *)
        echo "❌ Invalid EXECUTION_MODE: ${EXECUTION_MODE}"
        echo "Valid options: once, daily, cron"
        exit 1
        ;;
esac