#!/bin/bash

# 🏥 MedraN Medical AI Assistant - Simple Startup Script
# This script automatically starts all services needed for MedraN

set -e

# Color codes for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   🏥  MedraN Medical AI Assistant                           ║"
echo "║                                                              ║"
echo "║       Starting your medical AI assistant...                 ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Docker is installed and running
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Error: Docker is not installed${NC}"
    echo -e "${YELLOW}💡 Please install Docker Desktop first:${NC}"
    echo -e "${CYAN}   • Windows/Mac: https://www.docker.com/products/docker-desktop${NC}"
    echo -e "${CYAN}   • Linux: Follow instructions at https://docs.docker.com/engine/install/${NC}"
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}❌ Error: Docker is not running${NC}"
    echo -e "${YELLOW}💡 Please start Docker Desktop and try again${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker is installed and running${NC}"

# Check if docker-compose is available (try both docker-compose and docker compose)
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    echo -e "${RED}❌ Error: docker-compose is not available${NC}"
    echo -e "${YELLOW}💡 Please install docker-compose or use a newer version of Docker${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker Compose is available${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down MedraN services...${NC}"
    ./docker-start.sh down
    echo -e "${PURPLE}👋 Thank you for using MedraN Medical AI Assistant!${NC}"
}

# Trap Ctrl+C
trap cleanup SIGINT

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}🚀 Starting MedraN Medical AI Assistant...${NC}"
echo -e "${CYAN}📍 Working directory: $SCRIPT_DIR${NC}"
echo ""

# Check if docker-start.sh exists
if [ ! -f "docker-start.sh" ]; then
    echo -e "${RED}❌ Error: docker-start.sh not found${NC}"
    echo -e "${YELLOW}💡 Please run this script from the MedraN project directory${NC}"
    exit 1
fi

# Make docker-start.sh executable
chmod +x docker-start.sh

# Check for existing containers and stop them if running
echo -e "${YELLOW}🔍 Checking for existing containers...${NC}"
if docker ps -a --filter "name=medran" --format "table {{.Names}}\t{{.Status}}" | grep -v NAMES | grep -q .; then
    echo -e "${YELLOW}🛑 Stopping existing containers...${NC}"
    ./docker-start.sh down
    echo -e "${GREEN}✅ Cleaned up existing containers${NC}"
fi

# Clear ChromaDB collections if needed
echo -e "${YELLOW}🗂️  Checking if collection reset is needed...${NC}"
read -p "$(echo -e ${CYAN})Reset vector database collections? This fixes embedding dimension mismatches. (y/N): $(echo -e ${NC})" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}🗑️  Collections will be cleared automatically when the system starts${NC}"
    # Create a flag file to indicate collections should be cleared
    touch .clear_collections
fi

# Start services
echo -e "${GREEN}🚀 Starting all services...${NC}"
echo -e "${CYAN}   This may take a few minutes for the first startup${NC}"
echo -e "${CYAN}   Models will be downloaded automatically if needed${NC}"
echo ""

# Start with automatic GPU detection
./docker-start.sh -d

# Wait a moment for containers to start
echo -e "${YELLOW}⏳ Waiting for services to initialize...${NC}"
sleep 10

# Check if services are running
echo -e "${BLUE}🔍 Checking service status...${NC}"
if docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -q "Up"; then
    echo -e "${GREEN}✅ Services are starting up!${NC}"
    echo ""
    
    # Show running containers
    echo -e "${CYAN}📊 Running services:${NC}"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | head -n 20
    echo ""
    
    # Wait for health check
    echo -e "${YELLOW}🏥 Waiting for health check...${NC}"
    for i in {1..60}; do
        if curl -s http://localhost:3000/api/healthz > /dev/null 2>&1; then
            echo -e "${GREEN}✅ MedraN is healthy and ready!${NC}"
            break
        fi
        if [ $i -eq 60 ]; then
            echo -e "${YELLOW}⚠️  Health check timed out, but services might still be starting${NC}"
        fi
        echo -n "."
        sleep 2
    done
    echo ""
    
    # Success message
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║   🎉  MedraN Medical AI Assistant is ready!                 ║"
    echo "║                                                              ║"
    echo "║   🌐  Open your browser and visit:                          ║"
    echo "║       http://localhost:3000                                  ║"
    echo "║                                                              ║"
    echo "║   📚  Upload documents, chat with AI, use voice features!   ║"
    echo "║                                                              ║"
    echo "║   🛑  Press Ctrl+C to stop all services                     ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Open browser (optional)
    echo -e "${CYAN}🌐 Would you like to open MedraN in your browser? (y/N): ${NC}"
    read -p "" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v xdg-open > /dev/null; then
            xdg-open http://localhost:3000
        elif command -v open > /dev/null; then
            open http://localhost:3000
        elif command -v start > /dev/null; then
            start http://localhost:3000
        else
            echo -e "${YELLOW}💡 Please open http://localhost:3000 in your browser${NC}"
        fi
    fi
    
    # Show logs
    echo -e "${CYAN}📋 Showing recent logs (press Ctrl+C to stop logs, services will keep running):${NC}"
    echo ""
    ./docker-start.sh logs -f
    
else
    echo -e "${RED}❌ Services failed to start properly${NC}"
    echo -e "${YELLOW}💡 Checking logs for errors...${NC}"
    ./docker-start.sh logs --tail=50
    exit 1
fi
