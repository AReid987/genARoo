"""
SQLAlchemy database models for Roo Code persistence layer.
"""

import enum
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Enum as SQLAlchemyEnum,
    Boolean,
)
from sqlalchemy.orm import relationship

from app.database import Base


class ProjectStatus(enum.Enum):
    """Project status enumeration."""
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class EpicStatus(enum.Enum):
    """Epic status enumeration."""
    BACKLOG = "backlog"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    CANCELLED = "cancelled"


class TaskStatus(enum.Enum):
    """Task status enumeration."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class TaskPriority(enum.Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Project(Base):
    """
    Project model representing a high-level project or initiative.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(SQLAlchemyEnum(ProjectStatus), default=ProjectStatus.PLANNING, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    epics = relationship("Epic", back_populates="project", cascade="all, delete-orphan")


class Epic(Base):
    """
    Epic model representing a large feature or capability within a project.
    """
    __tablename__ = "epics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(SQLAlchemyEnum(EpicStatus), default=EpicStatus.BACKLOG, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="epics")
    tasks = relationship("Task", back_populates="epic", cascade="all, delete-orphan")


class Task(Base):
    """
    Task model representing individual work items within an epic.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority = Column(SQLAlchemyEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    complexity = Column(Integer, nullable=True)  # 1-10 complexity score
    epic_id = Column(Integer, ForeignKey("epics.id"), nullable=False)
    assignee = Column(String(255), nullable=True)  # Could be agent name or user
    estimated_hours = Column(Integer, nullable=True)
    actual_hours = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    epic = relationship("Epic", back_populates="tasks")


class AgentState(Base):
    """
    AgentState model for tracking the current state and context of AI agents.
    """
    __tablename__ = "agent_states"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(255), nullable=False, unique=True, index=True)
    current_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    current_project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    context_data = Column(Text, nullable=True)  # JSON string for flexible context storage
    last_activity = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    current_task = relationship("Task", foreign_keys=[current_task_id])
    current_project = relationship("Project", foreign_keys=[current_project_id])


class Roomode(Base):
    """
    Roomode model representing a specialized AI agent or functional unit.
    """
    __tablename__ = "roomodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    type = Column(String(50), nullable=False)  # e.g., "Orchestrator", "Planning", "Coding"
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    memory_entries = relationship("MemoryEntry", back_populates="roomode", cascade="all, delete-orphan")


class MemoryEntry(Base):
    """
    MemoryEntry model for storing pieces of information in the Memory Bank.
    """
    __tablename__ = "memory_entries"

    id = Column(Integer, primary_key=True, index=True)
    roomode_id = Column(Integer, ForeignKey("roomodes.id"), nullable=False)
    type = Column(String(50), nullable=False)  # e.g., "Global", "Local", "Scratchpad", "LongTerm"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    related_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    related_project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    embedding = Column(Text, nullable=True)  # Store vector embeddings as JSON string or similar
    metadata_json = Column(Text, nullable=True)  # Flexible JSON field for additional metadata

    # Relationships
    roomode = relationship("Roomode", back_populates="memory_entries")
    related_task = relationship("Task", foreign_keys=[related_task_id])
    related_project = relationship("Project", foreign_keys=[related_project_id])
