# 1. Use a minimal, secure base image
FROM python:3.11-slim-bookworm

# 2. Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Install only essential security updates and clean up to keep the image tiny
RUN apt-get update && apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 4. Create a non-privileged group and user
# We use --system to ensure this user has no login shell or unnecessary home folder access
RUN groupadd --system sandboxgroup && \
    useradd --system --gid sandboxgroup --create-home --home-dir /home/sandboxuser sandboxuser

# 5. Set up the working directory
WORKDIR /app

# 6. Change ownership of the app directory to the non-root user
RUN chown -R sandboxuser:sandboxgroup /app

# 7. Switch to the non-root user for all subsequent operations
USER sandboxuser

# 8. This container's job is to stay alive so the FastAPI server can "exec" commands into it.
# 'tail -f /dev/null' is a standard way to keep a container running without consuming CPU.
CMD ["tail", "-f", "/dev/null"]