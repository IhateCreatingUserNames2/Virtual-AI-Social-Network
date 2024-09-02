# Deployment script 
#!/bin/bash

# deploy.sh

# Ensure the script exits on any error
set -e

# Function to display usage instructions
usage() {
    echo "Usage: $0 {start|stop|restart|status|migrate|logs}"
    exit 1
}

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Start the application
start() {
    echo "Starting the application..."
    gunicorn --workers 4 --bind 0.0.0.0:8000 main:app --log-level=info --access-logfile logs/access.log --error-logfile logs/error.log &
    echo $! > gunicorn.pid
    echo "Application started."
}

# Stop the application
stop() {
    if [ -f gunicorn.pid ]; then
        echo "Stopping the application..."
        kill -9 $(cat gunicorn.pid)
        rm -f gunicorn.pid
        echo "Application stopped."
    else
        echo "No application is currently running."
    fi
}

# Restart the application
restart() {
    echo "Restarting the application..."
    stop
    start
    echo "Application restarted."
}

# Show the status of the application
status() {
    if [ -f gunicorn.pid ]; then
        if ps -p $(cat gunicorn.pid) > /dev/null; then
            echo "Application is running."
        else
            echo "Application is not running."
        fi
    else
        echo "Application is not running."
    fi
}

# Apply database migrations
migrate() {
    echo "Applying database migrations..."
    alembic upgrade head
    echo "Database migrations applied."
}

# Show the application logs
logs() {
    echo "Showing application logs..."
    tail -f logs/access.log logs/error.log
}

# Ensure the logs directory exists
mkdir -p logs

# Handle script arguments
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    migrate)
        migrate
        ;;
    logs)
        logs
        ;;
    *)
        usage
        ;;
esac
