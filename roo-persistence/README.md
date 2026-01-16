# Roo Persistence Layer

A FastAPI-based database persistence layer for Roo Code, built as a Turborepo monorepo with Python and TypeScript packages.

## Overview

This project provides a robust database persistence layer for the Roo Code application, enabling storage, retrieval, and management of operational data including projects, epics, tasks, agent state, and other relevant information.

## Architecture

- **FastAPI**: Web API framework
- **SQLAlchemy**: Object-Relational Mapper (ORM)
- **Pydantic**: Data validation and serialization
- **SQLite**: Database engine (file-based)
- **Uvicorn**: ASGI server
- **Turborepo**: Monorepo build system
- **PDM & UV**: Python package management
- **PNPM**: Node.js package management

## Project Structure

```ini
roo-persistence/
├── apps/
│   └── api/                 # FastAPI application
├── packages/
│   ├── db/                  # Database models and utilities
│   └── schemas/             # Shared Pydantic schemas
├── tools/
│   └── scripts/             # Build and utility scripts
├── turbo.json              # Turborepo configuration
├── package.json            # Root package.json
├── pnpm-workspace.yaml     # PNPM workspace configuration
└── pyproject.toml          # Python project configuration
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- PNPM
- PDM
- UV

### Installation

```bash
# Install Node.js dependencies
pnpm install

# Install Python dependencies
pdm install

# Initialize database
pdm run init-db

# Start development server
pnpm dev
```

## Development

### Running the API

```bash
# Development mode with hot reload
pnpm dev:api

# Production mode
pnpm start:api
```

### Testing

```bash
# Run all tests
pnpm test

# Run Python tests only
pdm run test

# Run with coverage
pdm run test:coverage
```

### Database Management

```bash
# Initialize database
pdm run init-db

# Reset database
pdm run reset-db

# Run migrations (future)
pdm run migrate
```

## API Documentation

Once running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

MIT
