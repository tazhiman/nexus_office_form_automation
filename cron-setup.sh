#!/bin/bash

# Nexus Form Automation - Cron Setup Script for Ubuntu
# This script sets up daily execution at 6:00 AM using system cron

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/automation_logs"

echo "🚀 Setting up Nexus Form Automation Cron Job"
echo "📁 Project directory: $SCRIPT_DIR"
echo "📄 Log directory: $LOG_DIR"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Create the cron script
cat > "$SCRIPT_DIR/run_daily_automation.sh" << 'EOF'
#!/bin/bash

# Daily automation execution script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "⏰ Starting daily automation at $(date)" >> automation_logs/daily_cron.log

# Run the Docker container for single execution
docker-compose -f docker-compose.lightweight.yml run --rm \
    -e EXECUTION_MODE=once \
    nexus-form-automation >> automation_logs/daily_cron.log 2>&1

echo "✅ Daily automation completed at $(date)" >> automation_logs/daily_cron.log
echo "===========================================" >> automation_logs/daily_cron.log
EOF

# Make the script executable
chmod +x "$SCRIPT_DIR/run_daily_automation.sh"

# Add cron job for 6:00 AM daily
CRON_JOB="0 6 * * * $SCRIPT_DIR/run_daily_automation.sh"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "$SCRIPT_DIR/run_daily_automation.sh"; then
    echo "⚠️  Cron job already exists. Removing old entry..."
    crontab -l 2>/dev/null | grep -v "$SCRIPT_DIR/run_daily_automation.sh" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Cron job added successfully!"
echo "📅 Schedule: Daily at 6:00 AM"
echo "📋 Command: $SCRIPT_DIR/run_daily_automation.sh"
echo ""
echo "To verify the cron job:"
echo "  crontab -l"
echo ""
echo "To view logs:"
echo "  tail -f $LOG_DIR/daily_cron.log"
echo ""
echo "To remove the cron job:"
echo "  crontab -l | grep -v '$SCRIPT_DIR/run_daily_automation.sh' | crontab -"