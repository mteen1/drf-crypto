# justfile

# Set environment variables
set dotenv-load

# Build the Docker images
build:
    docker compose -f docker-compose.local.yml build

migrations:
    docker compose -f docker-compose.local.yml run --rm django python manage.py makemigrations

# Run the Docker containers
run:
    docker compose -f docker-compose.local.yml up

# Run Detached
rund:
    docker compose -f docker-compose.local.yml up -d

# Stop the Docker containers
stop:
    docker compose -f docker-compose.local.yml down

exec:
    docker compose -f docker-compose.local.yml run django bash

# Run Telegram Bot
bot:
    docker compose -f docker-compose.local.yml run --rm django python manage.py run_telegram_bot

# Run tests using pytest
test:
    docker compose -f docker-compose.local.yml run --rm django pytest

# Run tests with coverage
coverage:
    docker compose -f docker-compose.local.yml run --rm django coverage run -m pytest
    docker compose -f docker-compose.local.yml run --rm django coverage html
    open htmlcov/index.html

# Run type checks with mypy
type-check:
    docker compose -f docker-compose.local.yml run --rm django mypy nems

# Create a superuser
superuser:
    docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser
# Kubernetes commands
k8s-apply:
    kubectl apply -f kubernetes/

k8s-delete:
    kubectl delete -f kubernetes/

k8s-status:
    kubectl get all