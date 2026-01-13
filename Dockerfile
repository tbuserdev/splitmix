# syntax=docker/dockerfile:1.4
FROM python:3.11-slim

# Install ffmpeg (required for audio processing)
# Using cache mount to speed up repeated builds
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends ffmpeg

WORKDIR /app

# Install uv for fast Python package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy ONLY dependency files first (maximizes cache hits)
COPY pyproject.toml .

# Install dependencies with uv (much faster than pip)
# Cache mount keeps downloaded packages between builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --compile-bytecode -r pyproject.toml

# Copy application code LAST (changes frequently, should not bust dep cache)
COPY main.py app.py downloader.py ./

# Create data directory
RUN mkdir -p /app/data

# Expose Streamlit port
EXPOSE 8501

# Health check (using python instead of curl to avoid extra dependency)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
