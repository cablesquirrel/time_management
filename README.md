# Time Management

## Description

API service to automate tracking and enforcement of time limits.

Set a default balance and add or remove time. When time runs out, or the timer is paused, actions can run to trigger an external process.

In this case, I'm using this as a way to set an 'internet time' limit for a teenager. They get a daily balance of time.

- When the timer is started, a remote API call is made to Ansible AWX to enable a switch port feeding their devices
- When the balance is depleted, or the timer is paused, a call is made to disable their switch port
- More time can be added to the balance, or the balance can be set to a smaller or lager amount

## Pre-commit checks

This repo is enabled with pre-commit checks

You can run these manually by executing

```bash
pre-commit run --all-files
```

## Running locally

```bash
# Create the virtual environment in the project
uv venv

# Start a shell in the virtual environment
source .venv/bin/activate

# Sync local packages with list from this repo
uv sync

# Use the included .vscode/launch.json configuration in VSCode to run the API
```

## Image building

```bash
docker build -t ghcr.io/<username>/time-management:latest --progress=plain .
docker push ghcr.io/<username>/time-management:latest
```

## Running image locally

```bash
docker run --rm  --name time-mgmt ghcr.io/<username>/time-management:latest
```

To enter the container, use

```bash
docker exec -it time-mgmt /bin/bash
```
