# justfile for yukichan-bot-v2

default:
    @just --list

# Run the bot in development mode
dev:
    uv run python bot.py

# Run unit tests
test:
    uv run pytest

# Run unit tests with coverage
test-cov:
    uv run pytest --cov=src

# Build production release package
build:
    ./build.sh

# Clean build artifacts, temporary caches, and dist packages
clean:
    rm -rf dist build *.egg-info .pytest_cache .coverage
