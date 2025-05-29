#!/bin/bash
# 🚀 Start AI Trading Orchestrator

echo "🧠 AI Trading Orchestrator Startup Script"
echo "=========================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "💡 Please copy env.example to .env and configure your API keys"
    echo "   cp env.example .env"
    echo "   nano .env  # Edit with your API keys"
    exit 1
fi

# Check if GROQ_API_KEY is set
if ! grep -q "GROQ_API_KEY=your_groq_api_key_here" .env; then
    echo "✅ GROQ_API_KEY appears to be configured"
else
    echo "⚠️  WARNING: GROQ_API_KEY still has default value"
    echo "   Please set your real Groq API key in .env file"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs/orchestrator
mkdir -p data/orchestrator
mkdir -p data/prometheus
mkdir -p data/grafana

# Set permissions
echo "🔧 Setting permissions..."
sudo chown -R 472:472 data/grafana 2>/dev/null || echo "  (Grafana permissions - OK if fails)"

# Start the system
echo "🚀 Starting AI Trading Orchestrator..."
echo ""

# Start only the orchestrator service
docker-compose up -d ai_orchestrator

echo ""
echo "✅ AI Orchestrator started successfully!"
echo ""
echo "🔗 Available endpoints:"
echo "   📊 Status: http://localhost:8080/status"
echo "   💚 Health: http://localhost:8080/health"  
echo "   📈 Metrics: http://localhost:8080/metrics"
echo "   📜 Decisions: http://localhost:8080/decisions"
echo ""
echo "📋 Useful commands:"
echo "   docker-compose logs -f ai_orchestrator  # View logs"
echo "   docker-compose stop ai_orchestrator     # Stop orchestrator"
echo "   docker-compose restart ai_orchestrator  # Restart orchestrator"
echo ""
echo "🎯 The AI is now making intelligent trading decisions!"
echo "   It will automatically switch between Crypto and Forex based on market conditions." 