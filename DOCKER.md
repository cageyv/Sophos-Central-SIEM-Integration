# Docker Deployment Guide

## Overview

This service runs continuously in a Docker container using Google's distroless Python image for minimal attack surface and enhanced security.

## Features

- **Distroless base image**: Minimal Google distroless Python image (no shell, package manager, or unnecessary tools)
- **Continuous execution**: Runs automatically every 10 minutes (no crontab needed)
- **Multi-architecture**: Supports `linux/amd64` and `linux/arm64`
- **CI/CD**: Automated builds via GitHub Actions on push to main/master or tag release

## Quick Start

### 1. Prepare Configuration

```bash
cp config.ini.sample config.ini
# Edit config.ini with your API credentials
```

### 2. Create Required Directories

```bash
mkdir -p state log
```

### 3. Run with Docker Compose

```bash
docker-compose up -d
```

### 4. View Logs

```bash
docker-compose logs -f sophos-siem
```

## Manual Docker Run

```bash
docker run -d \
  --name sophos-siem \
  --restart unless-stopped \
  -v $(pwd)/config.ini:/app/config.ini:ro \
  -v $(pwd)/state:/app/state \
  -v $(pwd)/log:/app/log \
  -e SOPHOS_SIEM_HOME=/app \
  -e SIEM_INTERVAL=600 \
  ghcr.io/cageyv/sophos-central-siem:latest
```

## Building Locally

```bash
docker build -t sophos-central-siem:local .
```

## Environment Variables

- `SOPHOS_SIEM_HOME`: Application home directory (default: `/app`)
- `PYTHONUNBUFFERED`: Force Python to run in unbuffered mode for real-time logs
- `SIEM_INTERVAL`: Execution interval in seconds (default: `600` = 10 minutes)

## Volumes

- `/app/config.ini` - Configuration file (required, read-only recommended)
- `/app/state` - Persistent state files to track progress
- `/app/log` - Application logs (if file logging is configured)

## Execution Interval

The service runs `siem.py` every **10 minutes** (600 seconds) by default. To change this interval, set the `SIEM_INTERVAL` environment variable (in seconds) in `docker-compose.yml` or pass it via `-e SIEM_INTERVAL=300` to `docker run`.

## CI/CD Pipeline

The GitHub Actions workflow automatically:
- Builds Docker images on push to `main`/`master` branches
- Builds and tags on version tags (`v*.*.*`)
- Pushes to GitHub Container Registry (`ghcr.io`)
- Creates multi-architecture images (amd64, arm64)
- Tags images with:
  - `latest` - Latest build from main/master
  - `<branch>` - Branch name
  - `<sha>` - Git commit SHA
  - `<semver>` - Semantic version (if tagged)

## Monitoring

Check container status:
```bash
docker-compose ps
```

Follow logs:
```bash
docker-compose logs -f
```

Check resource usage:
```bash
docker stats sophos-siem
```

## Troubleshooting

**Container exits immediately:**
- Verify `config.ini` exists and is properly configured
- Check logs: `docker-compose logs sophos-siem`

**No data being collected:**
- Verify API credentials in `config.ini`
- Check network connectivity from container
- Review state file in `./state/` directory

**High resource usage:**
- Adjust execution interval in `run_loop.py`
- Enable resource limits in `docker-compose.yml`

## Security Notes

- Distroless images contain only runtime dependencies (no shell, package manager)
- Runs as non-root user by default
- Config file should be mounted read-only (`:ro`)
- Keep API credentials secure and never commit to version control

