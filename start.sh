#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🏠 Drawing to 3D House Design - Startup Script${NC}"
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}❌ Error: backend/.env file not found!${NC}"
    echo "Please create it from backend/.env.example and add your ANTHROPIC_API_KEY"
    exit 1
fi

# Check if ANTHROPIC_API_KEY is set
if ! grep -q "ANTHROPIC_API_KEY=sk-" backend/.env 2>/dev/null; then
    echo -e "${RED}⚠️  Warning: ANTHROPIC_API_KEY may not be configured in backend/.env${NC}"
    echo "Make sure to add your API key before the application will work properly"
    echo ""
fi

echo -e "${GREEN}✅ Starting backend server...${NC}"
# Start backend in background
source venv/bin/activate
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 3

echo -e "${GREEN}✅ Starting frontend development server...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${GREEN}🎉 Application started!${NC}"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${BLUE}Stopping servers...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Wait for both processes
wait
