# 🚀 Nexus Form Automation - Ubuntu Deployment Guide

This guide provides detailed instructions for deploying the lightweight Nexus Form Automation to run daily at 6:00 AM on Ubuntu.

## 📋 Prerequisites

### System Requirements
- **Ubuntu 20.04 LTS or 22.04 LTS**
- **Minimum 1GB RAM** (2GB recommended)
- **1GB free disk space**
- **Internet connection**
- **Docker and Docker Compose installed**

### Install Docker (if not already installed)
```bash
# Update package index
sudo apt update

# Install Docker
sudo apt install -y docker.io docker-compose

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER

# Log out and back in, or run:
newgrp docker

# Verify installation
docker --version
docker-compose --version
```

## 🏗️ Deployment Options

### Option 1: Docker Compose with Built-in Scheduler (Recommended)

This option runs a persistent container that executes the automation daily at 6:00 AM.

#### Step 1: Deploy the Project
```bash
# Clone or download the project files
mkdir -p ~/nexus-automation
cd ~/nexus-automation

# Copy all project files to this directory:
# - form_automation_lightweight.py
# - Dockerfile.lightweight
# - docker-compose.lightweight.yml
# - requirements_lightweight.txt
# - run_automation.sh

# Make sure run_automation.sh is executable
chmod +x run_automation.sh
```

#### Step 2: Configure Environment Variables
```bash
# Edit docker-compose.lightweight.yml to customize your settings
nano docker-compose.lightweight.yml

# Key environment variables to modify:
# - VISITOR_NAME: Your name
# - COMPANY: Your company name
# - MOBILE: Your mobile number
# - ACCESS_LEVEL: Your access level (1-5)
# - PURPOSE: Purpose of visit (Meeting, Delivery, Training, etc.)
# - TZ: Your timezone (e.g., Asia/Singapore, America/New_York)
```

#### Step 3: Build and Start the Container
```bash
# Build the Docker image
docker-compose -f docker-compose.lightweight.yml build

# Start the container in daily mode
docker-compose -f docker-compose.lightweight.yml up -d

# Check container status
docker-compose -f docker-compose.lightweight.yml ps

# View logs
docker-compose -f docker-compose.lightweight.yml logs -f
```

#### Step 4: Monitor the Automation
```bash
# Check logs directory
ls -la automation_logs/

# View latest execution logs
tail -f automation_logs/form_automation_*.log

# View container logs
docker logs nexus-form-automation -f
```

### Option 2: System Cron with Docker (Alternative)

This option uses Ubuntu's system cron to run the automation daily.

#### Step 1: Set Up Project Files
```bash
# Create project directory
mkdir -p ~/nexus-automation
cd ~/nexus-automation

# Copy all project files here
# Make scripts executable
chmod +x run_automation.sh
chmod +x cron-setup.sh
```

#### Step 2: Run Cron Setup Script
```bash
# Execute the cron setup script
./cron-setup.sh

# This will:
# - Create a daily execution script
# - Add a cron job for 6:00 AM daily
# - Set up logging
```

#### Step 3: Verify Cron Setup
```bash
# Check if cron job was added
crontab -l

# You should see:
# 0 6 * * * /home/username/nexus-automation/run_daily_automation.sh

# Test the automation manually
./run_daily_automation.sh
```

## 🔧 Configuration

### Environment Variables Reference

| Variable | Description | Default Value | Examples |
|----------|-------------|---------------|----------|
| `VISITOR_NAME` | Your full name | Rizwan Ahamed | John Doe, Mary Smith |
| `ACCESS_LEVEL` | Office access level | 5 | 1, 2, 3, 4, 5 |
| `PURPOSE` | Visit purpose | Meeting | Meeting, Delivery, Training, Interview |
| `COMPANY` | Your company name | Cognizant | Microsoft, Google, Local Corp |
| `MOBILE` | Your mobile number | 87686853 | 87654321, +1234567890 |
| `ADDITIONAL_INFO` | Extra information | Daily automated... | Project meeting, Client visit |
| `TZ` | Timezone | Asia/Singapore | America/New_York, Europe/London |
| `EXECUTION_MODE` | When to run | daily | once, daily, cron |

### Customizing Execution Time

To change from 6:00 AM to a different time:

**For Docker Compose method:**
```bash
# Edit the container's internal scheduler
# You'll need to modify run_automation.sh
nano run_automation.sh
# Change target_hour=6 to your desired hour (24-hour format)
```

**For System Cron method:**
```bash
# Edit the cron job
crontab -e
# Change "0 6 * * *" to your desired time
# Format: minute hour day month dayofweek
# Examples:
# 0 8 * * *   = 8:00 AM daily
# 30 7 * * *  = 7:30 AM daily
# 0 18 * * 1-5 = 6:00 PM weekdays only
```

## 📊 Monitoring and Troubleshooting

### View Logs
```bash
# Container logs (Docker Compose method)
docker logs nexus-form-automation

# Application logs
tail -f automation_logs/form_automation_*.log

# Cron logs (System Cron method)
tail -f automation_logs/daily_cron.log

# System cron logs
grep CRON /var/log/syslog
```

### Check Container Health
```bash
# Container status
docker ps

# Container resource usage
docker stats nexus-form-automation

# Container health check
docker inspect nexus-form-automation | grep -A 10 Health
```

### Common Issues and Solutions

#### Issue: Container fails to start
```bash
# Check Docker logs
docker logs nexus-form-automation

# Rebuild container
docker-compose -f docker-compose.lightweight.yml build --no-cache
docker-compose -f docker-compose.lightweight.yml up -d
```

#### Issue: Chrome/ChromeDriver errors
```bash
# Check Chrome installation in container
docker exec nexus-form-automation google-chrome --version
docker exec nexus-form-automation chromedriver --version

# Rebuild with latest Chrome
docker-compose -f docker-compose.lightweight.yml build --no-cache
```

#### Issue: Cron job not running
```bash
# Check if cron service is running
sudo systemctl status cron

# Start cron if stopped
sudo systemctl start cron

# Check cron logs
grep CRON /var/log/syslog | tail -20
```

## 🔄 Maintenance

### Update the Automation
```bash
# Pull latest changes
cd ~/nexus-automation

# Update configuration if needed
nano docker-compose.lightweight.yml

# Rebuild and restart
docker-compose -f docker-compose.lightweight.yml down
docker-compose -f docker-compose.lightweight.yml build --no-cache
docker-compose -f docker-compose.lightweight.yml up -d
```

### Clean Up Old Logs
```bash
# Remove logs older than 30 days
find automation_logs/ -name "*.log" -mtime +30 -delete
find automation_logs/ -name "*.json" -mtime +30 -delete
```

### Backup Configuration
```bash
# Create backup of configuration
tar -czf nexus-automation-backup-$(date +%Y%m%d).tar.gz \
    docker-compose.lightweight.yml \
    form_automation_lightweight.py \
    automation_logs/
```

## 🛡️ Security Considerations

### Container Security
- Container runs as non-root user
- Security options enabled: `no-new-privileges`
- Resource limits configured
- Minimal attack surface (lightweight base image)

### Network Security
- Container doesn't expose any ports
- Uses host network only for outbound connections
- No incoming network access required

### Data Security
- No sensitive data stored in container
- Logs are mounted to host filesystem
- Environment variables can be secured using Docker secrets

## 📈 Performance Optimization

### Resource Limits
Current configuration:
- **Memory**: 512MB limit, 256MB reserved
- **CPU**: 0.5 cores limit, 0.25 cores reserved

To adjust:
```yaml
# In docker-compose.lightweight.yml
deploy:
  resources:
    limits:
      memory: 1G        # Increase if needed
      cpus: '1.0'       # Increase if needed
```

### Log Rotation
```bash
# Configure log rotation
sudo nano /etc/logrotate.d/nexus-automation

# Add content:
/home/username/nexus-automation/automation_logs/*.log {
    daily
    missingok
    rotate 30
    compress
    notifempty
    create 644 username username
}
```

## 🆘 Support and Troubleshooting

### Quick Health Check
```bash
# Run this script to check system health
#!/bin/bash
echo "=== Nexus Automation Health Check ==="
echo "Docker status: $(systemctl is-active docker)"
echo "Container status: $(docker inspect nexus-form-automation --format='{{.State.Status}}' 2>/dev/null || echo 'Not running')"
echo "Last log entry: $(ls -t automation_logs/*.log 2>/dev/null | head -1 | xargs tail -1 2>/dev/null || echo 'No logs found')"
echo "Cron jobs: $(crontab -l | grep nexus 2>/dev/null || echo 'No cron jobs')"
echo "Disk space: $(df -h . | tail -1 | awk '{print $5 " used"}')"
```

### Get Help
1. Check the logs first: `automation_logs/`
2. Verify configuration: `docker-compose.lightweight.yml`
3. Test manually: `docker-compose -f docker-compose.lightweight.yml run --rm -e EXECUTION_MODE=once nexus-form-automation`
4. Check container health: `docker inspect nexus-form-automation`

## 🎯 Success Verification

After deployment, verify everything is working:

1. **Container is running**: `docker ps | grep nexus`
2. **Logs are being created**: `ls -la automation_logs/`
3. **Cron job exists**: `crontab -l` (if using cron method)
4. **Manual test succeeds**: Run a test execution
5. **Wait for scheduled run**: Check logs after 6:00 AM next day

Your Nexus Form Automation is now ready for daily automated execution! 🎉