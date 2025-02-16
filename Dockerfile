# Build stage
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install build dependencies and create wheels
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.11-slim

# Create non-root user for security
RUN useradd -m appuser && \
    mkdir -p /app && \
    chown appuser:appuser /app

# Set working directory
WORKDIR /app

# Copy wheels from builder stage
COPY --from=builder /app/wheels /wheels

# Copy project files
COPY src/ src/
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache /wheels/* && \
    rm -rf /wheels && \
    # Create log directory with proper permissions
    mkdir -p /app/logs && \
    chown -R appuser:appuser /app/logs

# Switch to non-root user
USER appuser

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production

# Command to run the bot
CMD ["python", "-m", "src.bot"]