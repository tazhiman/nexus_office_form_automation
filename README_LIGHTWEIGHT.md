# 🐳 Nexus Form Automation - Lightweight Containerized Version

## 📁 Files Created

This lightweight version consists of the following files:

### Core Application Files
- **`form_automation_lightweight.py`** - Main automation script optimized for containers
- **`requirements_lightweight.txt`** - Python dependencies (minimal)
- **`run_automation.sh`** - Container execution script with scheduling logic

### Docker Configuration
- **`Dockerfile.lightweight`** - Ubuntu-based container with Chrome/ChromeDriver
- **`docker-compose.lightweight.yml`** - Complete deployment configuration
- **`.env.example`** - Environment variables template

### Setup and Deployment
- **`quick-setup.sh`** - Automated setup script for easy deployment
- **`cron-setup.sh`** - System cron setup for backup scheduling
- **`DEPLOYMENT_GUIDE.md`** - Comprehensive deployment instructions

## 🚀 Quick Start (3 Simple Steps)

### Option 1: Automated Setup (Recommended)
```bash
# 1. Copy all files to your Ubuntu server
scp -r * user@your-server:~/nexus-automation/

# 2. SSH to your server and run setup
ssh user@your-server
cd ~/nexus-automation
chmod +x quick-setup.sh
./quick-setup.sh

# 3. Done! The automation will run daily at 6:00 AM
```

### Option 2: Manual Setup
```bash
# 1. Install Docker (if not installed)
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
newgrp docker

# 2. Deploy the application
cd ~/nexus-automation
docker-compose -f docker-compose.lightweight.yml up -d

# 3. Check status
docker-compose -f docker-compose.lightweight.yml ps
```

## ⚙️ Configuration

Edit `docker-compose.lightweight.yml` to customize:

```yaml
environment:
  - VISITOR_NAME=Your Name Here
  - COMPANY=Your Company
  - MOBILE=Your Mobile Number
  - ACCESS_LEVEL=5
  - PURPOSE=Meeting
  - TZ=Your/Timezone
```

## 📊 Key Features

### ✅ Optimized for Production
- **Resource Efficient**: Uses <512MB RAM
- **No Screenshots**: Logs only for minimal disk usage
- **Headless Operation**: No GUI required
- **Health Monitoring**: Built-in health checks
- **Automatic Restart**: Container restarts on failure

### ✅ Flexible Scheduling
- **Daily Mode**: Runs at 6:00 AM every day
- **Manual Mode**: Run once and exit
- **Cron Mode**: Use system cron for backup scheduling

### ✅ Comprehensive Logging
- **Execution Logs**: Detailed step-by-step logs
- **JSON Reports**: Structured execution data
- **Error Tracking**: Full error logging and debugging
- **Log Rotation**: Automatic cleanup of old logs

### ✅ Security & Reliability
- **Non-root User**: Container runs as unprivileged user
- **Resource Limits**: Memory and CPU limits configured
- **Health Checks**: Automatic container health monitoring
- **Error Recovery**: Graceful error handling and reporting

## 📈 Monitoring

### View Logs
```bash
# Application logs
tail -f automation_logs/form_automation_*.log

# Container logs
docker logs nexus-form-automation -f

# Execution reports
cat automation_logs/execution_log_*.json | jq .
```

### Check Status
```bash
# Container status
docker ps | grep nexus

# Resource usage
docker stats nexus-form-automation

# Health status
docker inspect nexus-form-automation | grep -A 5 Health
```

## 🔧 Management Commands

```bash
# Start automation
docker-compose -f docker-compose.lightweight.yml up -d

# Stop automation
docker-compose -f docker-compose.lightweight.yml down

# View logs
docker-compose -f docker-compose.lightweight.yml logs -f

# Run manual test
docker-compose -f docker-compose.lightweight.yml run --rm \
  -e EXECUTION_MODE=once nexus-form-automation

# Update configuration
docker-compose -f docker-compose.lightweight.yml down
# Edit docker-compose.lightweight.yml
docker-compose -f docker-compose.lightweight.yml up -d

# Rebuild container (after code changes)
docker-compose -f docker-compose.lightweight.yml build --no-cache
docker-compose -f docker-compose.lightweight.yml up -d
```

## 🛠️ Troubleshooting

### Container Won't Start
```bash
# Check Docker logs
docker logs nexus-form-automation

# Rebuild container
docker-compose -f docker-compose.lightweight.yml build --no-cache
```

### Automation Fails
```bash
# Check application logs
tail -f automation_logs/form_automation_*.log

# Run manual test with debugging
docker-compose -f docker-compose.lightweight.yml run --rm \
  -e EXECUTION_MODE=once \
  -e LOG_LEVEL=DEBUG \
  nexus-form-automation
```

### Performance Issues
```bash
# Monitor resource usage
docker stats nexus-form-automation

# Increase resource limits in docker-compose.lightweight.yml
# memory: 1G
# cpus: '1.0'
```

## 📅 Scheduling Options

### Change Execution Time
Edit `run_automation.sh` and modify:
```bash
target_hour=8  # Change from 6 to 8 for 8:00 AM
target_minute=30  # Change from 0 to 30 for 8:30 AM
```

### Use System Cron Instead
```bash
# Run the cron setup script
./cron-setup.sh

# Or manually add cron job
crontab -e
# Add: 0 6 * * * /path/to/your/project/run_daily_automation.sh
```

### Run on Weekdays Only
Edit cron job:
```bash
0 6 * * 1-5  # Monday to Friday only
```

## 🔒 Security Features

- **Container Security**: Runs as non-root user
- **Resource Isolation**: Memory and CPU limits
- **Network Security**: No exposed ports
- **Minimal Attack Surface**: Lightweight base image
- **No Sensitive Data**: All configuration via environment variables

## 📦 Resource Requirements

- **RAM**: 256MB minimum, 512MB recommended
- **CPU**: 0.25 cores minimum, 0.5 cores recommended  
- **Disk**: 100MB for application, 50MB for logs (with rotation)
- **Network**: Outbound HTTPS access required

## 🆘 Support

For detailed troubleshooting and deployment instructions, see:
- **`DEPLOYMENT_GUIDE.md`** - Complete deployment guide
- **Container logs** - `docker logs nexus-form-automation`
- **Application logs** - `automation_logs/` directory

## ✨ Success Indicators

Your automation is working correctly when you see:
1. ✅ Container status: "Up" in `docker ps`
2. ✅ Recent logs in `automation_logs/`
3. ✅ "Form automation completed successfully!" in logs
4. ✅ JSON execution reports with `"success": true`

---

**Your containerized Nexus Form Automation is ready for production deployment! 🚀**