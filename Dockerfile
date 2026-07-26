FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Install system dependencies required by cairosvg (libcairo2) and ffmpeg (optional for yt-dlp)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcairo2 \
    ffmpeg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy dependency files first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies into virtualenv
RUN uv sync --frozen --no-install-project --no-dev

# Copy application source code
COPY . .

# Install project
RUN uv sync --frozen --no-dev

# Expose default NoneBot port
EXPOSE 8080

CMD ["uv", "run", "python", "bot.py"]
