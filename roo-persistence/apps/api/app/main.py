"""
Main FastAPI application for Roo Code persistence layer.
"""

from datetime import datetime, timezone
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import __version__
from app.database import init_db, get_db
from app.routers import projects, epics, tasks, agent_state, roomodes, memory_entries
from app.schemas import HealthCheck


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    print("🚀 Starting Roo Code Persistence API...")
    try:
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        raise

    yield

    # Shutdown
    print("🛑 Shutting down Roo Code Persistence API...")


# Create FastAPI application
app = FastAPI(
    title="Roo Code Persistence API",
    description="A robust database persistence layer for Roo Code application",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router, prefix="/api/v1")
app.include_router(epics.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(agent_state.router, prefix="/api/v1")
app.include_router(roomodes.router, prefix="/api/v1")
app.include_router(memory_entries.router, prefix="/api/v1")


@app.get("/", response_model=dict)
async def root():
    """
    Root endpoint providing basic API information.

    Returns:
        Basic API information
    """
    return {
        "name": "Roo Code Persistence API",
        "version": __version__,
        "description": "A robust database persistence layer for Roo Code application",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "health_check": "/health",
    }


@app.get("/health", response_model=HealthCheck)
async def health_check():
    return {"status": "ok"}


# Error handlers are handled by FastAPI automatically
# Custom error handlers can be added here if needed


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
