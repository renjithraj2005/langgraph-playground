.PHONY: install run dev clean format lint test

# Default target
all: install

# Install dependencies
install:
	poetry install

# Run the application
run:
	PYTHONDONTWRITEBYTECODE=1 poetry run python run.py

# Run in development mode with auto-reload
dev:
	PYTHONDONTWRITEBYTECODE=1 poetry run python run.py

# Run the search agent
search:
	PYTHONDONTWRITEBYTECODE=1 poetry run python -m salonist.cli search "$(filter-out $@,$(MAKECMDGOALS))"

# Visualize the workflow graph
visualize:
	PYTHONDONTWRITEBYTECODE=1 poetry run flask visualize-graph

# Clean up Python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +

# Format code using black
format:
	PYTHONDONTWRITEBYTECODE=1 poetry run black .

# Run linting
lint:
	PYTHONDONTWRITEBYTECODE=1 poetry run flake8 .
	PYTHONDONTWRITEBYTECODE=1 poetry run black --check .

# Run tests
test:
	PYTHONDONTWRITEBYTECODE=1 poetry run pytest

# Create a new virtual environment and install dependencies
setup:
	poetry env remove --all
	poetry install

# Show Poetry environment info
env-info:
	poetry env info

# Show Poetry dependencies
deps:
	poetry show

# Update dependencies
update:
	poetry update

# Export requirements.txt
export:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

# Create .env file with PYTHONDONTWRITEBYTECODE setting
init-env:
	echo "PYTHONDONTWRITEBYTECODE=1" >> .env 