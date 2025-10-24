#!/bin/bash

# Script to run the Raman ML classification tool in Docker

set -e  # Exit on any error

echo "=== Raman ML Classification - Docker Setup ==="
echo ""

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

# Check if we need to rebuild
if [ "$1" = "--rebuild" ] || [ "$1" = "-r" ]; then
    echo "🔄 Rebuilding Docker image..."
    docker-compose build --no-cache
    echo "✅ Image rebuilt successfully"
else
    echo "📦 Using existing image (use --rebuild to force rebuild)"
fi

# Stop any existing container
echo "🛑 Stopping any existing container..."
docker-compose down >/dev/null 2>&1 || true

# Start the container
echo "🚀 Starting container..."
docker-compose up -d

# Wait a moment for container to be ready
sleep 2

# Check if container is running
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Container failed to start. Check logs with: docker-compose logs"
    exit 1
fi

echo "✅ Container is running!"
echo ""
echo "📊 You can now run your ML classification commands:"
echo "   python ml-classification_v2.0.py --models rf --cv loocv --train EXAMPLE_CSV.csv"
echo ""
echo "📈 Plots will be saved as PNG files (Docker-friendly)"
echo "   Run 'python view_plots.py' to see available plot files"
echo "   Use 'docker cp raman-ml:/app/<filename>.png .' to copy plots to host"
echo ""
echo "🔧 Usage:"
echo "   ./run_docker.sh        - Start with existing image"
echo "   ./run_docker.sh --rebuild - Rebuild image (if you changed requirements.txt or Dockerfile)"
echo ""

# Get into the container
echo "🐳 Entering the container..."
docker-compose exec ml-classification bash
