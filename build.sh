#!/usr/bin/env bash
set -e

# Determine version from parameter or pyproject.toml
if [ -n "$1" ]; then
    VERSION="$1"
else
    VERSION=$(grep -m1 '^version =' pyproject.toml | cut -d '"' -f 2)
fi

TARGET_NAME="yukichan-bot-v2"
ARCHIVE_NAME="${TARGET_NAME}-v${VERSION}.tar.gz"
DIST_DIR="dist"

echo "=========================================="
echo " Building ${TARGET_NAME} (version: v${VERSION}) "
echo "=========================================="

# Create dist directory
mkdir -p "${DIST_DIR}"

# Archive package contents into dist/
tar -czf "${DIST_DIR}/${ARCHIVE_NAME}" \
    --exclude='.git' \
    --exclude='.venv' \
    --exclude='.pytest_cache' \
    --exclude='.coverage' \
    --exclude='__pycache__' \
    --exclude='*/__pycache__' \
    --exclude='dist' \
    bot.py \
    src \
    docs \
    Dockerfile \
    docker-compose.yaml \
    pyproject.toml \
    uv.lock \
    justfile \
    README.md \
    .env.example \
    .editorconfig \
    .gitattributes

echo "Build complete: ${DIST_DIR}/${ARCHIVE_NAME}"
ls -lh "${DIST_DIR}/${ARCHIVE_NAME}"
