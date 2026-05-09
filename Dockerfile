# =========================
# Base Image
# =========================
FROM python:3.11-slim-bookworm

# =========================
# Environment Variables
# =========================
ENV PYTHONDWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# =========================
# System Dependencies + Docker CLI
# =========================
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    ca-certificates \
    gnupg \
    lsb-release \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update && apt-get install -y docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Install uv
# =========================
RUN pip install --no-cache-dir uv

# =========================
# Working Directory
# =========================
WORKDIR /app

# =========================
# Copy Project Files
# =========================
COPY . .

# =========================
# Install Python Dependencies
# =========================
RUN uv pip install --system -r requirements.txt

# =========================
# Expose Ports
# =========================
EXPOSE 8080
EXPOSE 8501

# =========================
# Startup Script
# =========================
RUN chmod +x start.sh

# =========================
# Start FastAPI + Streamlit
# =========================
CMD ["bash", "start.sh"]