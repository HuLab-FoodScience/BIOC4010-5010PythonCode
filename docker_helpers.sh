#!/bin/bash

# Helper script for common Docker operations

case "$1" in
    "start")
        echo "🚀 Starting container..."
        docker-compose up -d
        echo "✅ Container started. Use 'docker-compose exec ml-classification bash' to enter."
        ;;
    "stop")
        echo "🛑 Stopping container..."
        docker-compose down
        echo "✅ Container stopped."
        ;;
    "restart")
        echo "🔄 Restarting container..."
        docker-compose down
        docker-compose up -d
        echo "✅ Container restarted."
        ;;
    "logs")
        echo "📋 Container logs:"
        docker-compose logs ml-classification
        ;;
    "status")
        echo "📊 Container status:"
        docker-compose ps
        ;;
    "clean")
        echo "🧹 Cleaning up..."
        docker-compose down --volumes --remove-orphans
        docker system prune -f
        echo "✅ Cleanup complete."
        ;;
    "copy-plots")
        echo "📈 Copying plots to host..."
        docker cp raman-ml:/app/cv_results_loocv.png . 2>/dev/null || echo "No cv_results_loocv.png found"
        docker cp raman-ml:/app/external_test_results.png . 2>/dev/null || echo "No external_test_results.png found"
        echo "✅ Plots copied to current directory."
        ;;
    *)
        echo "🔧 Docker Helper Commands:"
        echo "  ./docker_helpers.sh start     - Start container"
        echo "  ./docker_helpers.sh stop      - Stop container"
        echo "  ./docker_helpers.sh restart   - Restart container"
        echo "  ./docker_helpers.sh logs     - View container logs"
        echo "  ./docker_helpers.sh status   - Check container status"
        echo "  ./docker_helpers.sh clean    - Clean up everything"
        echo "  ./docker_helpers.sh copy-plots - Copy plot files to host"
        ;;
esac
