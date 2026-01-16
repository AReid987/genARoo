"""
Pydantic schemas for API request/response validation and serialization.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

from app.models import ProjectStatus, EpicStatus, TaskStatus, TaskPriority


# Base schemas
class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    model_config = ConfigDict(from_attributes=True)


# Project schemas
class ProjectBase(BaseSchema):
    """Base project schema with common fields."""
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    status: ProjectStatus = Field(default=ProjectStatus.PLANNING, description="Project status")


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    pass


class ProjectUpdate(BaseSchema):
    """Schema for updating an existing project."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    status: Optional[ProjectStatus] = Field(None, description="Project status")


class ProjectRead(ProjectBase):
    """Schema for reading project data."""
    id: int = Field(..., description="Project ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class ProjectReadWithEpics(ProjectRead):
    """Schema for reading project data with associated epics."""
    epics: List["EpicRead"] = Field(default=[], description="Associated epics")


# Epic schemas
class EpicBase(BaseSchema):
    """Base epic schema with common fields."""
    title: str = Field(..., min_length=1, max_length=255, description="Epic title")
    description: Optional[str] = Field(None, description="Epic description")
    status: EpicStatus = Field(default=EpicStatus.BACKLOG, description="Epic status")


class EpicCreate(EpicBase):
    """Schema for creating a new epic."""
    project_id: int = Field(..., description="Associated project ID")


class EpicUpdate(BaseSchema):
    """Schema for updating an existing epic."""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Epic title")
    description: Optional[str] = Field(None, description="Epic description")
    status: Optional[EpicStatus] = Field(None, description="Epic status")
    project_id: Optional[int] = Field(None, description="Associated project ID")


class EpicRead(EpicBase):
    """Schema for reading epic data."""
    id: int = Field(..., description="Epic ID")
    project_id: int = Field(..., description="Associated project ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class EpicReadWithTasks(EpicRead):
    """Schema for reading epic data with associated tasks."""
    tasks: List["TaskRead"] = Field(default=[], description="Associated tasks")


# Task schemas
class TaskBase(BaseSchema):
    """Base task schema with common fields."""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.TODO, description="Task status")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority")
    complexity: Optional[int] = Field(None, ge=1, le=10, description="Task complexity (1-10)")
    assignee: Optional[str] = Field(None, max_length=255, description="Task assignee")
    estimated_hours: Optional[int] = Field(None, ge=0, description="Estimated hours")
    actual_hours: Optional[int] = Field(None, ge=0, description="Actual hours")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    epic_id: int = Field(..., description="Associated epic ID")


class TaskUpdate(BaseSchema):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: Optional[TaskStatus] = Field(None, description="Task status")
    priority: Optional[TaskPriority] = Field(None, description="Task priority")
    complexity: Optional[int] = Field(None, ge=1, le=10, description="Task complexity (1-10)")
    epic_id: Optional[int] = Field(None, description="Associated epic ID")
    assignee: Optional[str] = Field(None, max_length=255, description="Task assignee")
    estimated_hours: Optional[int] = Field(None, ge=0, description="Estimated hours")
    actual_hours: Optional[int] = Field(None, ge=0, description="Actual hours")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")


class TaskRead(TaskBase):
    """Schema for reading task data."""
    id: int = Field(..., description="Task ID")
    epic_id: int = Field(..., description="Associated epic ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")


# Agent State schemas
class AgentStateBase(BaseSchema):
    """Base agent state schema with common fields."""
    agent_id: str = Field(..., min_length=1, max_length=255, description="Unique agent identifier")
    current_task_id: Optional[int] = Field(None, description="Current task ID")
    current_project_id: Optional[int] = Field(None, description="Current project ID")
    context_data: Optional[str] = Field(None, description="Agent context data (JSON)")
    is_active: bool = Field(default=True, description="Whether agent is active")


class AgentStateCreate(AgentStateBase):
    """Schema for creating a new agent state."""
    pass


class AgentStateUpdate(BaseSchema):
    """Schema for updating an existing agent state."""
    current_task_id: Optional[int] = Field(None, description="Current task ID")
    current_project_id: Optional[int] = Field(None, description="Current project ID")
    context_data: Optional[str] = Field(None, description="Agent context data (JSON)")
    is_active: Optional[bool] = Field(None, description="Whether agent is active")


class AgentStateRead(AgentStateBase):
    """Schema for reading agent state data."""
    id: int = Field(..., description="Agent state ID")
    last_activity: datetime = Field(..., description="Last activity timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


# Roomode schemas
class RoomodeBase(BaseSchema):
    """Base roomode schema with common fields."""
    name: str = Field(..., description="Roomode name")
    description: Optional[str] = Field(None, description="Roomode description")
    type: str = Field(..., description="Roomode type")
    is_active: bool = Field(default=True, description="Whether roomode is active")


class RoomodeCreate(RoomodeBase):
    """Schema for creating a new roomode."""
    pass


class RoomodeUpdate(BaseSchema):
    """Schema for updating an existing roomode."""
    name: Optional[str] = Field(None, description="Roomode name")
    description: Optional[str] = Field(None, description="Roomode description")
    type: Optional[str] = Field(None, description="Roomode type")
    is_active: Optional[bool] = Field(None, description="Whether roomode is active")


class RoomodeRead(RoomodeBase):
    """Schema for reading roomode data."""
    id: int = Field(..., description="Roomode ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


# Memory Entry schemas
class MemoryEntryBase(BaseSchema):
    """Base memory entry schema with common fields."""
    roomode_id: int = Field(..., description="Associated roomode ID")
    type: str = Field(..., description="Type of memory entry")
    content: str = Field(..., description="Content of the memory entry")
    related_task_id: Optional[int] = Field(None, description="Associated task ID")
    related_project_id: Optional[int] = Field(None, description="Associated project ID")
    embedding: Optional[str] = Field(None, description="Vector embedding of the content (e.g., JSON or base64)")
    metadata_json: Optional[str] = Field(None, description="Additional metadata as JSON string")


class MemoryEntryCreate(MemoryEntryBase):
    """Schema for creating a new memory entry."""
    pass


class MemoryEntryUpdate(BaseSchema):
    """Schema for updating an existing memory entry."""
    roomode_id: Optional[int] = Field(None, description="Associated roomode ID")
    type: Optional[str] = Field(None, description="Type of memory entry")
    content: Optional[str] = Field(None, description="Content of the memory entry")
    related_task_id: Optional[int] = Field(None, description="Associated task ID")
    related_project_id: Optional[int] = Field(None, description="Associated project ID")
    embedding: Optional[str] = Field(None, description="Vector embedding of the content (e.g., JSON or base64)")
    metadata_json: Optional[str] = Field(None, description="Additional metadata as JSON string")


class MemoryEntryRead(MemoryEntryBase):
    """Schema for reading memory entry data."""
    id: int = Field(..., description="Memory entry ID")
    timestamp: datetime = Field(..., description="Timestamp of the memory entry")


# Pagination schemas
class PaginationParams(BaseSchema):
    """Schema for pagination parameters."""
    skip: int = Field(default=0, ge=0, description="Number of records to skip")
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum number of records to return")


class PaginatedResponse(BaseSchema):
    """Base schema for paginated responses."""
    total: int = Field(..., description="Total number of records")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Maximum number of records returned")


class PaginatedProjectsResponse(PaginatedResponse):
    """Schema for paginated projects response."""
    items: List[ProjectRead] = Field(..., description="List of projects")


class PaginatedEpicsResponse(PaginatedResponse):
    """Schema for paginated epics response."""
    items: List[EpicRead] = Field(..., description="List of epics")


class PaginatedTasksResponse(PaginatedResponse):
    """Schema for paginated tasks response."""
    items: List[TaskRead] = Field(..., description="List of tasks")


# Health check schema
class HealthCheck(BaseSchema):
    """Schema for health check response."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")
    database: str = Field(..., description="Database status")
