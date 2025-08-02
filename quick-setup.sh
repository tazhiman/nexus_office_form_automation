#!/bin/bash

# Nexus Form Automation - Quick Setup Script
# This script automates the entire deployment process

set -e

echo "🚀 Nexus Form Automation - Quick Setup"
echo "======================================"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed!"
        echo "Please install Docker first:"
        echo "  sudo apt update"
        echo "  sudo apt install -y docker.io docker-compose"
        echo "  sudo usermod -aG docker \$USER"
        echo "  newgrp docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed!"
        echo "Please install Docker Compose first:"
        echo "  sudo apt install -y docker-compose"
        exit 1
    fi
    
    print_status "Docker and Docker Compose are installed"
}

# Create project directory
setup_directory() {
    PROJECT_DIR="$HOME/nexus-automation"
    
    if [ -d "$PROJECT_DIR" ]; then
        print_warning "Directory $PROJECT_DIR already exists"
        read -p "Do you want to continue and overwrite? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Setup cancelled."
            exit 1
        fi
    fi
    
    mkdir -p "$PROJECT_DIR"
    cd "$PROJECT_DIR"
    print_status "Project directory created: $PROJECT_DIR"
}

# Collect user information
collect_user_info() {
    echo ""
    echo "📋 Please provide your information for form automation:"
    echo "=================================================="
    
    read -p "👤 Your full name [Rizwan Ahamed]: " USER_NAME
    USER_NAME=${USER_NAME:-"Rizwan Ahamed"}
    
    read -p "🏢 Your company [Cognizant]: " USER_COMPANY
    USER_COMPANY=${USER_COMPANY:-"Cognizant"}
    
    read -p "📱 Your mobile number [87686853]: " USER_MOBILE
    USER_MOBILE=${USER_MOBILE:-"87686853"}
    
    echo "🎯 Select your visit purpose:"
    echo "  1) Meeting (default)"
    echo "  2) Delivery"
    echo "  3) Training"
    echo "  4) Interview"
    echo "  5) Other"
    read -p "Choice [1]: " PURPOSE_CHOICE
    PURPOSE_CHOICE=${PURPOSE_CHOICE:-1}
    
    case $PURPOSE_CHOICE in
        1) USER_PURPOSE="Meeting" ;;
        2) USER_PURPOSE="Delivery" ;;
        3) USER_PURPOSE="Training" ;;
        4) USER_PURPOSE="Interview" ;;
        5) 
            read -p "Enter custom purpose: " USER_PURPOSE
            USER_PURPOSE=${USER_PURPOSE:-"Meeting"}
            ;;
        *) USER_PURPOSE="Meeting" ;;
    esac
    
    echo "🔐 Select your access level:"
    echo "  1) Level 1"
    echo "  2) Level 2" 
    echo "  3) Level 3"
    echo "  4) Level 4"
    echo "  5) Level 5 (default)"
    read -p "Choice [5]: " ACCESS_CHOICE
    ACCESS_CHOICE=${ACCESS_CHOICE:-5}
    
    echo "⏰ Select execution schedule:"
    echo "  1) Daily at 6:00 AM (default)"
    echo "  2) Custom time"
    echo "  3) Manual execution only"
    read -p "Choice [1]: " SCHEDULE_CHOICE
    SCHEDULE_CHOICE=${SCHEDULE_CHOICE:-1}
    
    if [ "$SCHEDULE_CHOICE" == "2" ]; then
        read -p "Enter hour (0-23) [6]: " CUSTOM_HOUR
        CUSTOM_HOUR=${CUSTOM_HOUR:-6}
        read -p "Enter minute (0-59) [0]: " CUSTOM_MINUTE
        CUSTOM_MINUTE=${CUSTOM_MINUTE:-0}
    fi
    
    print_status "Information collected"
}

# Create configuration files
create_config() {
    # Create docker-compose file with user's information
    cat > docker-compose.yml << EOF
version: '3.8'

services:
  nexus-form-automation:
    build:
      context: .
      dockerfile: Dockerfile.lightweight
    container_name: nexus-form-automation
    restart: unless-stopped
    
    environment:
      - EXECUTION_MODE=daily
      - TZ=Asia/Singapore
      - VISITOR_NAME=$USER_NAME
      - ACCESS_LEVEL=$ACCESS_CHOICE
      - PURPOSE=$USER_PURPOSE
      - COMPANY=$USER_COMPANY
      - MOBILE=$USER_MOBILE
      - ADDITIONAL_INFO=Daily automated visitor registration
      - FORM_URL=https://forms.office.com/Pages/ResponsePage.aspx?id=WGeXB8aT70uz3FOGA9yRbsbr_tTOC29AvupnhyEvx8FUNlFMQlVGMFNQUjJNUFZOTUJTMlk0SElTWSQlQCN0PWcu&origin=QRCode
    
    volumes:
      - ./automation_logs:/app/logs
    
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
    
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    
    healthcheck:
      test: ["CMD", "python3", "-c", "import selenium; print('OK')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
    security_opt:
      - no-new-privileges:true

volumes:
  automation_logs:
    driver: local
EOF

    # Create environment file for easy editing
    cat > .env << EOF
# Nexus Form Automation Configuration
# Edit these values as needed

VISITOR_NAME=$USER_NAME
COMPANY=$USER_COMPANY
MOBILE=$USER_MOBILE
PURPOSE=$USER_PURPOSE
ACCESS_LEVEL=$ACCESS_CHOICE
ADDITIONAL_INFO=Daily automated visitor registration

# Timezone (change as needed)
TZ=Asia/Singapore

# Form URL (don't change unless you have a different form)
FORM_URL=https://forms.office.com/Pages/ResponsePage.aspx?id=WGeXB8aT70uz3FOGA9yRbsbr_tTOC29AvupnhyEvx8FUNlFMQlVGMFNQUjJNUFZOTUJTMlk0SElTWSQlQCN0PWcu&origin=QRCode

# Execution mode: once, daily, cron
EXECUTION_MODE=daily
EOF

    print_status "Configuration files created"
}

# Copy necessary files (assuming they're in the same directory as this script)
copy_files() {
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # List of files to copy
    FILES=(
        "form_automation_lightweight.py"
        "Dockerfile.lightweight"
        "requirements_lightweight.txt"
        "run_automation.sh"
    )
    
    for file in "${FILES[@]}"; do
        if [ -f "$SCRIPT_DIR/$file" ]; then
            cp "$SCRIPT_DIR/$file" .
            print_status "Copied $file"
        else
            print_error "Missing file: $file"
            echo "Please ensure all required files are in the same directory as this setup script."
            exit 1
        fi
    done
    
    # Make scripts executable
    chmod +x run_automation.sh
    
    # Create logs directory
    mkdir -p automation_logs
}

# Build and start the container
deploy_container() {
    print_info "Building Docker container..."
    docker-compose build
    
    print_info "Starting container..."
    docker-compose up -d
    
    # Wait a moment for container to start
    sleep 5
    
    # Check if container is running
    if docker-compose ps | grep -q "Up"; then
        print_status "Container is running successfully!"
    else
        print_error "Container failed to start. Check logs:"
        docker-compose logs
        exit 1
    fi
}

# Setup system cron (optional)
setup_cron() {
    if [ "$SCHEDULE_CHOICE" == "3" ]; then
        print_info "Skipping cron setup (manual execution mode selected)"
        return
    fi
    
    if [ "$SCHEDULE_CHOICE" == "2" ]; then
        CRON_TIME="$CUSTOM_MINUTE $CUSTOM_HOUR * * *"
        TIME_DESC="$CUSTOM_HOUR:$(printf %02d $CUSTOM_MINUTE)"
    else
        CRON_TIME="0 6 * * *"
        TIME_DESC="6:00 AM"
    fi
    
    echo ""
    read -p "Do you want to set up system cron for backup scheduling? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Create backup cron script
        cat > run_daily_backup.sh << EOF
#!/bin/bash
cd "$PROJECT_DIR"
echo "⏰ Backup execution at \$(date)" >> automation_logs/backup_cron.log
docker-compose run --rm -e EXECUTION_MODE=once nexus-form-automation >> automation_logs/backup_cron.log 2>&1
echo "===========================================" >> automation_logs/backup_cron.log
EOF
        chmod +x run_daily_backup.sh
        
        # Add to cron
        (crontab -l 2>/dev/null | grep -v "$PROJECT_DIR/run_daily_backup.sh"; echo "$CRON_TIME $PROJECT_DIR/run_daily_backup.sh") | crontab -
        
        print_status "Backup cron job created for $TIME_DESC"
    fi
}

# Show final instructions
show_instructions() {
    echo ""
    echo "🎉 Setup Complete!"
    echo "=================="
    echo ""
    echo "📁 Project location: $PROJECT_DIR"
    echo "👤 Configured for: $USER_NAME ($USER_COMPANY)"
    echo "📱 Mobile: $USER_MOBILE"
    echo "🎯 Purpose: $USER_PURPOSE"
    echo "🔐 Access Level: $ACCESS_CHOICE"
    echo ""
    echo "🔧 Management Commands:"
    echo "======================"
    echo "View logs:      cd $PROJECT_DIR && tail -f automation_logs/*.log"
    echo "Check status:   cd $PROJECT_DIR && docker-compose ps"
    echo "View container logs: cd $PROJECT_DIR && docker-compose logs -f"
    echo "Stop automation: cd $PROJECT_DIR && docker-compose down"
    echo "Start automation: cd $PROJECT_DIR && docker-compose up -d"
    echo "Test manually:   cd $PROJECT_DIR && docker-compose run --rm -e EXECUTION_MODE=once nexus-form-automation"
    echo ""
    echo "📝 Configuration:"
    echo "=================="
    echo "Main config:     $PROJECT_DIR/docker-compose.yml"
    echo "Environment:     $PROJECT_DIR/.env"
    echo "To modify settings, edit these files and restart:"
    echo "  cd $PROJECT_DIR && docker-compose down && docker-compose up -d"
    echo ""
    echo "📊 Monitoring:"
    echo "=============="
    echo "The automation will run daily and create detailed logs."
    echo "Check automation_logs/ directory for execution results."
    echo ""
    print_status "Your Nexus Form Automation is now ready!"
    print_info "The first execution will happen at the next scheduled time."
}

# Main execution
main() {
    check_docker
    setup_directory
    collect_user_info
    copy_files
    create_config
    deploy_container
    setup_cron
    show_instructions
}

# Run main function
main "$@"