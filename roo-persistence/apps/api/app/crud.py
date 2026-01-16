"""
CRUD (Create, Read, Update, Delete) operations for database models.
"""

from datetime import datetime, timezone
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from . import models, schemas


# Project CRUD operations
def create_project(db: Session, project: schemas.ProjectCreate) -> models.Project:
    """Create a new project."""
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project(db: Session, project_id: int) -> Optional[models.Project]:
    """Get a project by ID."""
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_projects(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[models.ProjectStatus] = None
) -> Tuple[List[models.Project], int]:
    """Get projects with pagination and optional status filter."""
    query = db.query(models.Project)

    if status:
        query = query.filter(models.Project.status == status)

    total = query.count()
    projects = query.offset(skip).limit(limit).all()

    return projects, total


def update_project(
    db: Session,
    project_id: int,
    project_update: schemas.ProjectUpdate
) -> Optional[models.Project]:
    """Update a project."""
    db_project = get_project(db, project_id)
    if not db_project:
        return None

    update_data = project_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)

    db_project.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int) -> bool:
    """Delete a project."""
    db_project = get_project(db, project_id)
    if not db_project:
        return False

    db.delete(db_project)
    db.commit()
    return True


# Epic CRUD operations
def create_epic(db: Session, epic: schemas.EpicCreate) -> models.Epic:
    """Create a new epic."""
    db_epic = models.Epic(**epic.model_dump())
    db.add(db_epic)
    db.commit()
    db.refresh(db_epic)
    return db_epic


def get_epic(db: Session, epic_id: int) -> Optional[models.Epic]:
    """Get an epic by ID."""
    return db.query(models.Epic).filter(models.Epic.id == epic_id).first()


def get_epics(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    status: Optional[models.EpicStatus] = None
) -> Tuple[List[models.Epic], int]:
    """Get epics with pagination and optional filters."""
    query = db.query(models.Epic)

    if project_id:
        query = query.filter(models.Epic.project_id == project_id)

    if status:
        query = query.filter(models.Epic.status == status)

    total = query.count()
    epics = query.offset(skip).limit(limit).all()

    return epics, total


def update_epic(
    db: Session,
    epic_id: int,
    epic_update: schemas.EpicUpdate
) -> Optional[models.Epic]:
    """Update an epic."""
    db_epic = get_epic(db, epic_id)
    if not db_epic:
        return None

    update_data = epic_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_epic, field, value)

    db_epic.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_epic)
    return db_epic


def delete_epic(db: Session, epic_id: int) -> bool:
    """Delete an epic."""
    db_epic = get_epic(db, epic_id)
    if not db_epic:
        return False

    db.delete(db_epic)
    db.commit()
    return True


# Task CRUD operations
def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    """Create a new task."""
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# Roomode CRUD operations
def create_roomode(db: Session, roomode: schemas.RoomodeCreate) -> models.Roomode:
    """Create a new roomode."""
    db_roomode = models.Roomode(**roomode.model_dump())
    db.add(db_roomode)
    db.commit()
    db.refresh(db_roomode)
    return db_roomode


def get_roomode(db: Session, roomode_id: int) -> Optional[models.Roomode]:
    """Get a roomode by ID."""
    return db.query(models.Roomode).filter(models.Roomode.id == roomode_id).first()


def get_roomodes(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    is_active: Optional[bool] = None
) -> Tuple[List[models.Roomode], int]:
    """Get roomodes with pagination and optional filters."""
    query = db.query(models.Roomode)

    if type:
        query = query.filter(models.Roomode.type == type)

    if is_active is not None:
        query = query.filter(models.Roomode.is_active == is_active)

    total = query.count()
    roomodes = query.offset(skip).limit(limit).all()

    return roomodes, total


def update_roomode(
    db: Session,
    roomode_id: int,
    roomode_update: schemas.RoomodeUpdate
) -> Optional[models.Roomode]:
    """Update a roomode."""
    db_roomode = get_roomode(db, roomode_id)
    if not db_roomode:
        return None

    update_data = roomode_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_roomode, field, value)

    db_roomode.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_roomode)
    return db_roomode


def delete_roomode(db: Session, roomode_id: int) -> bool:
    """Delete a roomode."""
    db_roomode = get_roomode(db, roomode_id)
    if not db_roomode:
        return False

    db.delete(db_roomode)
    db.commit()
    return True


# MemoryEntry CRUD operations
def create_memory_entry(db: Session, memory_entry: schemas.MemoryEntryCreate) -> models.MemoryEntry:
    """Create a new memory entry."""
    db_memory_entry = models.MemoryEntry(**memory_entry.model_dump())
    db.add(db_memory_entry)
    db.commit()
    db.refresh(db_memory_entry)
    return db_memory_entry


def get_memory_entry(db: Session, memory_entry_id: int) -> Optional[models.MemoryEntry]:
    """Get a memory entry by ID."""
    return db.query(models.MemoryEntry).filter(models.MemoryEntry.id == memory_entry_id).first()


def get_memory_entries(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    roomode_id: Optional[int] = None,
    type: Optional[str] = None,
    related_task_id: Optional[int] = None,
    related_project_id: Optional[int] = None
) -> Tuple[List[models.MemoryEntry], int]:
    """Get memory entries with pagination and optional filters."""
    query = db.query(models.MemoryEntry)

    if roomode_id:
        query = query.filter(models.MemoryEntry.roomode_id == roomode_id)

    if type:
        query = query.filter(models.MemoryEntry.type == type)

    if related_task_id:
        query = query.filter(models.MemoryEntry.related_task_id == related_task_id)

    if related_project_id:
        query = query.filter(models.MemoryEntry.related_project_id == related_project_id)

    total = query.count()
    memory_entries = query.offset(skip).limit(limit).all()

    return memory_entries, total


def update_memory_entry(
    db: Session,
    memory_entry_id: int,
    memory_entry_update: schemas.MemoryEntryUpdate
) -> Optional[models.MemoryEntry]:
    """Update a memory entry."""
    db_memory_entry = get_memory_entry(db, memory_entry_id)
    if not db_memory_entry:
        return None

    update_data = memory_entry_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_memory_entry, field, value)

    db_memory_entry.timestamp = datetime.now(timezone.utc) # Update timestamp on modification
    db.commit()
    db.refresh(db_memory_entry)
    return db_memory_entry


def delete_memory_entry(db: Session, memory_entry_id: int) -> bool:
    """Delete a memory entry."""
    db_memory_entry = get_memory_entry(db, memory_entry_id)
    if not db_memory_entry:
        return False

    db.delete(db_memory_entry)
    db.commit()
    return True


def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    """Get a task by ID."""
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    epic_id: Optional[int] = None,
    status: Optional[models.TaskStatus] = None,
    priority: Optional[models.TaskPriority] = None,
    assignee: Optional[str] = None
) -> Tuple[List[models.Task], int]:
    """Get tasks with pagination and optional filters."""
    query = db.query(models.Task)

    if epic_id:
        query = query.filter(models.Task.epic_id == epic_id)

    if status:
        query = query.filter(models.Task.status == status)

    if priority:
        query = query.filter(models.Task.priority == priority)

    if assignee:
        query = query.filter(models.Task.assignee == assignee)

    total = query.count()
    tasks = query.offset(skip).limit(limit).all()

    return tasks, total


def update_task(
    db: Session,
    task_id: int,
    task_update: schemas.TaskUpdate
) -> Optional[models.Task]:
    """Update a task."""
    db_task = get_task(db, task_id)
    if not db_task:
        return None

    update_data = task_update.model_dump(exclude_unset=True)

    # Handle status change to DONE
    if update_data.get("status") == models.TaskStatus.DONE and db_task.status != models.TaskStatus.DONE:
        update_data["completed_at"] = datetime.now(timezone.utc)
    elif update_data.get("status") != models.TaskStatus.DONE and "completed_at" not in update_data:
        update_data["completed_at"] = None

    for field, value in update_data.items():
        setattr(db_task, field, value)

    db_task.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_task)
    return db_task


# Roomode CRUD operations
def create_roomode(db: Session, roomode: schemas.RoomodeCreate) -> models.Roomode:
    """Create a new roomode."""
    db_roomode = models.Roomode(**roomode.model_dump())
    db.add(db_roomode)
    db.commit()
    db.refresh(db_roomode)
    return db_roomode


def get_roomode(db: Session, roomode_id: int) -> Optional[models.Roomode]:
    """Get a roomode by ID."""
    return db.query(models.Roomode).filter(models.Roomode.id == roomode_id).first()


def get_roomodes(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    is_active: Optional[bool] = None
) -> Tuple[List[models.Roomode], int]:
    """Get roomodes with pagination and optional filters."""
    query = db.query(models.Roomode)

    if type:
        query = query.filter(models.Roomode.type == type)

    if is_active is not None:
        query = query.filter(models.Roomode.is_active == is_active)

    total = query.count()
    roomodes = query.offset(skip).limit(limit).all()

    return roomodes, total


def update_roomode(
    db: Session,
    roomode_id: int,
    roomode_update: schemas.RoomodeUpdate
) -> Optional[models.Roomode]:
    """Update a roomode."""
    db_roomode = get_roomode(db, roomode_id)
    if not db_roomode:
        return None

    update_data = roomode_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_roomode, field, value)

    db_roomode.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_roomode)
    return db_roomode


def delete_roomode(db: Session, roomode_id: int) -> bool:
    """Delete a roomode."""
    db_roomode = get_roomode(db, roomode_id)
    if not db_roomode:
        return False

    db.delete(db_roomode)
    db.commit()
    return True


# MemoryEntry CRUD operations
def create_memory_entry(db: Session, memory_entry: schemas.MemoryEntryCreate) -> models.MemoryEntry:
    """Create a new memory entry."""
    db_memory_entry = models.MemoryEntry(**memory_entry.model_dump())
    db.add(db_memory_entry)
    db.commit()
    db.refresh(db_memory_entry)
    return db_memory_entry


def get_memory_entry(db: Session, memory_entry_id: int) -> Optional[models.MemoryEntry]:
    """Get a memory entry by ID."""
    return db.query(models.MemoryEntry).filter(models.MemoryEntry.id == memory_entry_id).first()


def get_memory_entries(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    roomode_id: Optional[int] = None,
    type: Optional[str] = None,
    related_task_id: Optional[int] = None,
    related_project_id: Optional[int] = None
) -> Tuple[List[models.MemoryEntry], int]:
    """Get memory entries with pagination and optional filters."""
    query = db.query(models.MemoryEntry)

    if roomode_id:
        query = query.filter(models.MemoryEntry.roomode_id == roomode_id)

    if type:
        query = query.filter(models.MemoryEntry.type == type)

    if related_task_id:
        query = query.filter(models.MemoryEntry.related_task_id == related_task_id)

    if related_project_id:
        query = query.filter(models.MemoryEntry.related_project_id == related_project_id)

    total = query.count()
    memory_entries = query.offset(skip).limit(limit).all()

    return memory_entries, total


def update_memory_entry(
    db: Session,
    memory_entry_id: int,
    memory_entry_update: schemas.MemoryEntryUpdate
) -> Optional[models.MemoryEntry]:
    """Update a memory entry."""
    db_memory_entry = get_memory_entry(db, memory_entry_id)
    if not db_memory_entry:
        return None

    update_data = memory_entry_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_memory_entry, field, value)

    db_memory_entry.timestamp = datetime.now(timezone.utc) # Update timestamp on modification
    db.commit()
    db.refresh(db_memory_entry)
    return db_memory_entry


def delete_memory_entry(db: Session, memory_entry_id: int) -> bool:
    """Delete a memory entry."""
    db_memory_entry = get_memory_entry(db, memory_entry_id)
    if not db_memory_entry:
        return False

    db.delete(db_memory_entry)
    db.commit()
    return True


def delete_task(db: Session, task_id: int) -> bool:
    """Delete a task."""
    db_task = get_task(db, task_id)
    if not db_task:
        return False

    db.delete(db_task)
    db.commit()
    return True


# Agent State CRUD operations
def create_agent_state(db: Session, agent_state: schemas.AgentStateCreate) -> models.AgentState:
    """Create a new agent state."""
    db_agent_state = models.AgentState(**agent_state.model_dump())
    db.add(db_agent_state)
    db.commit()
    db.refresh(db_agent_state)
    return db_agent_state


def get_agent_state(db: Session, agent_id: str) -> Optional[models.AgentState]:
    """Get agent state by agent ID."""
    return db.query(models.AgentState).filter(models.AgentState.agent_id == agent_id).first()


def get_agent_state_by_id(db: Session, state_id: int) -> Optional[models.AgentState]:
    """Get agent state by state ID."""
    return db.query(models.AgentState).filter(models.AgentState.id == state_id).first()


def get_agent_states(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None
) -> Tuple[List[models.AgentState], int]:
    """Get agent states with pagination and optional filters."""
    query = db.query(models.AgentState)

    if is_active is not None:
        query = query.filter(models.AgentState.is_active == is_active)

    total = query.count()
    agent_states = query.offset(skip).limit(limit).all()

    return agent_states, total


def update_agent_state(
    db: Session,
    agent_id: str,
    agent_state_update: schemas.AgentStateUpdate
) -> Optional[models.AgentState]:
    """Update agent state."""
    db_agent_state = get_agent_state(db, agent_id)
    if not db_agent_state:
        return None

    update_data = agent_state_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_agent_state, field, value)

    db_agent_state.last_activity = datetime.now(timezone.utc)
    db_agent_state.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_agent_state)
    return db_agent_state


def delete_agent_state(db: Session, agent_id: str) -> bool:
    """Delete agent state."""
    db_agent_state = get_agent_state(db, agent_id)
    if not db_agent_state:
        return False

    db.delete(db_agent_state)
    db.commit()
    return True
