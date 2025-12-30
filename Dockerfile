# Multi-stage build for Google distroless Python image
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy application files
COPY *.py ./

# Create necessary directories
RUN mkdir -p /app/state /app/log

# Final stage - Google distroless
FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app

# Copy all Python files from builder
COPY --from=builder /app/*.py ./

# Set environment variables
ENV SOPHOS_SIEM_HOME=/app
ENV PYTHONUNBUFFERED=1

# Distroless images run as nonroot by default
# Create volume mount points for state and logs
VOLUME ["/app/state", "/app/log"]

# Run the wrapper script that executes siem.py in a loop
ENTRYPOINT ["python3", "/app/run_loop.py"]

