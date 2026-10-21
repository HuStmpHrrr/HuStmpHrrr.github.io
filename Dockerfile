# Build environment for the homepage. Rebuilt by .github/workflows/docker-image.yml.
FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git rsync ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
