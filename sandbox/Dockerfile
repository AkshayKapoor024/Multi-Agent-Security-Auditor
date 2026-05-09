# =========================
# VANTAGUARD SANDBOX IMAGE
# =========================

FROM python:3.11-slim-bookworm

# Prevent pyc generation and enable immediate logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create persistent user pip path
ENV PATH="/home/sandboxuser/.local/bin:$PATH"

# Install basic utilities
RUN apt-get update && apt-get install -y \
    iputils-ping \
    curl \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root sandbox user
RUN groupadd --system sandboxgroup && \
    useradd --system \
    --gid sandboxgroup \
    --create-home \
    --home-dir /home/sandboxuser \
    sandboxuser

# Working directory
WORKDIR /app

# Change ownership
RUN chown -R sandboxuser:sandboxgroup /app

# Switch to non-root user
USER sandboxuser

# =========================
# PREINSTALL COMMON MODULES
# =========================

RUN python3 -m pip install --user --no-cache-dir \
    requests \
    beautifulsoup4 \
    lxml \
    pyyaml \
    python-dotenv \
    flask \
    fastapi \
    uvicorn \
    aiohttp \
    httpx \
    cryptography \
    pyjwt \
    bcrypt \
    passlib \
    markdown \
    bleach \
    dill \
    joblib \
    numpy \
    pandas \
    scikit-learn

# Keep container alive for docker exec
CMD ["tail", "-f", "/dev/null"]