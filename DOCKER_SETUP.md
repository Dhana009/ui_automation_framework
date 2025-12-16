# Docker Setup Guide

## Overview

The framework uses Docker to ensure consistent test execution across all environments (local, CI/CD, different machines). This eliminates system dependency issues and environment inconsistencies.

## Docker Image Details

**Base Image**: `mcr.microsoft.com/playwright/python:v1.45.0-jammy`
- Official Playwright Python image
- Pre-installed with all Playwright dependencies
- Ubuntu 22.04 (Jammy) base
- Python 3.11

**What's Included**:
- Python 3.11
- Playwright browsers (Chromium, Firefox, WebKit) pre-installed
- All system dependencies for running browsers
- pip package manager

## Local Development with Docker

### Build the Docker Image

```bash
docker build -t ui-automation-framework:latest .
```

### Run Tests in Docker

**Basic test run:**
```bash
docker run --rm ui-automation-framework:latest pytest tests/smoke/
```

**With custom pytest arguments:**
```bash
docker run --rm ui-automation-framework:latest pytest tests/smoke/ -v --tb=short
```

**With volume mount (save reports locally):**
```bash
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  ui-automation-framework:latest \
  pytest tests/smoke/ --html=reports/report.html --self-contained-html
```

**Interactive mode (for debugging):**
```bash
docker run -it --rm ui-automation-framework:latest bash
```

### View Reports After Test Run

Reports are saved to `reports/` directory (mounted volume) and can be viewed in your browser:
```bash
open reports/report.html  # macOS
xdg-open reports/report.html  # Linux
start reports/report.html  # Windows
```

## GitHub Actions Integration

The workflow automatically:
1. Builds the Docker image
2. Runs tests inside the container
3. Mounts the reports directory for artifact upload
4. Cleans up the container after tests

No additional setup needed - just push to GitHub!

## Troubleshooting

### Image won't build
```bash
# Clear Docker cache and rebuild
docker build --no-cache -t ui-automation-framework:latest .
```

### Tests run but screenshots/reports aren't saved
Make sure volume mount path is correct:
```bash
-v $(pwd)/reports:/app/reports
```

### Need to install additional system packages
Edit `Dockerfile` and add to the RUN command, then rebuild:
```dockerfile
RUN apt-get update && apt-get install -y <package-name>
```

### Running specific test file
```bash
docker run --rm ui-automation-framework:latest \
  pytest tests/smoke/test_playwright_docs.py -v
```

### Running tests with specific markers
```bash
docker run --rm ui-automation-framework:latest \
  pytest -m smoke -v
```

## Benefits Over Traditional Setup

✅ **Consistent Environment** - Same setup everywhere (local, CI/CD, teammates' machines)
✅ **Zero Dependency Issues** - No system package conflicts or missing dependencies
✅ **Easy Onboarding** - New developers just run: `docker build && docker run`
✅ **CI/CD Simplification** - GitHub Actions doesn't need complex dependency install steps
✅ **Reproducible Tests** - Failures can be debugged in identical container
✅ **Easy Scaling** - Run multiple containers in parallel for distributed testing

## Next Steps

- Tests run successfully in Docker
- Update team documentation to use Docker
- Consider Docker Compose for running with test databases/mock servers
- Add pre-commit hooks to rebuild image after Dockerfile changes

