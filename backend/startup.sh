#!/bin/bash
# Azure App Service startup script for SIGAP backend

# Run database migrations
python -m alembic upgrade head

# Start the application with gunicorn
exec gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:${PORT:-8000}
