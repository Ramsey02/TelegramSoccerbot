# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.11-slim
WORKDIR /app

# Copy project files maintaining structure
COPY --from=builder /app/wheels /wheels
COPY . .

# Install dependencies
RUN pip install --no-cache /wheels/* && \
    rm -rf /wheels

# Basic environment setup
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

EXPOSE 8443

# Change to source directory and run
WORKDIR /app/src
CMD ["python", "bot.py"]