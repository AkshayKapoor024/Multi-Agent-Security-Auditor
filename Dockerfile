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
# System Dependencies
# =========================
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
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