# Multi-Agent Task System

A multi-agent AI system for task management on Google Cloud.

## Overview

This repository contains a backend implementation for coordinating intelligent agents in a task management workflow. The system is built with:
- `FastAPI` for the API server
- Google Cloud Firestore for persistence
- Anthropic and AI tooling integrations for agent orchestration
- Modular agent components including note-taking, scheduling, and task planning

## Repository Structure

- `backend/`
  - `api/main.py` - FastAPI application entry point
  - `agents/` - Agent classes and orchestrator logic
    - `base_agent.py` - Common agent base functionality
    - `orchestrator.py` - Agent coordinator
    - `notes_agent.py` - Notes management agent
    - `schedule_agent.py` - Scheduling agent
    - `task_agent.py` - Task management agent
  - `config/settings.py` - Configuration and environment handling
  - `database/` - Firestore client and data models
  - `tools/` - Helper tools for calendar and task operations

- `tests/` - Unit tests for backend components

## Requirements

- Python 3.9+
- Google Cloud credentials for Firestore access
- `.env` with environment variables for configuration

## Installation

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend/requirements.txt
```

Alternatively, install from the project metadata:

```bash
pip install .
```

## Running the API

Start the FastAPI server from the repository root:

```bash
uvicorn backend.api.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Testing

Run tests using `pytest` from the repository root:

```bash
pytest
```

## Configuration

Configuration is loaded from environment variables and the `backend/config/settings.py` module. Common settings include:
- Firestore project and credentials
- Anthropic API key
- Any application-specific runtime settings

## Notes

- This project is designed for extension with additional agents and AI workflows.
- Use the `backend/agents/orchestrator.py` to modify task orchestration logic.

## License

MIT License
