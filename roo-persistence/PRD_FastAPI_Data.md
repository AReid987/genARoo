# Product Requirements Document: Roo Code - FastAPI Database Persistence Layer
Version: 1.0
Date: June 3, 2025
Author: Gemini AI (Collaboratively with User)

## 1. Introduction
This document outlines the requirements and design for a robust database persistence layer for the Roo Code application. The primary goal is to enable Roo Code to store, retrieve, and manage its operational data, including projects, epics, tasks, agent state, and other relevant information. This persistence layer will be implemented as a FastAPI application, providing a clear API for Roo Code's core logic to interact with the database. We will be using SQLite as the initial database backend, with SQLAlchemy as the ORM.

## 2. Goals
- Data Persistence: Ensure all critical Roo Code data is saved and can be retrieved across sessions.
- Structured Data Management: Organize data into well-defined entities (Projects, Epics, Tasks, Agent State, Memories, File Changes).
- Scalable Architecture: Implement a FastAPI-based service that can be scaled and maintained independently of the core Roo Code agent logic.
- Clear API Interface: Provide well-documented API endpoints for all CRUD (Create, Read, Update, Delete) operations.
- Modularity: Decouple data storage concerns from the agent's core processing logic.
- Developer-Friendly: Utilize Pydantic for data validation and serialization, and SQLAlchemy for ORM, offering a Pythonic development experience.

## 3. Target Users
- Primary: The Roo Code application itself (its various modules and "roomodes").
- Secondary: Developers working on Roo Code, who will interact with this data layer for development, debugging, and potential extensions.

## 4. Functional Requirements
### 4.1. Data Models
The system shall support the following data entities:

- Project: Represents a top-level initiative or piece of work.
  - Attributes: id, name, description, overall_goal, status, created_at, updated_at.

- Epic: A large body of work within a Project, composed of multiple Tasks.
  - Attributes: id, name, description, status, project_id (foreign key to Project), created_at, updated_at.

- Task: A specific, actionable item within an Epic.
  - Attributes: id, description, status, priority, epic_id (foreign key to Epic), created_at, updated_at.

- AgentState: Stores the current operational state of the Roo Code agent.
  - Attributes: id (can be a fixed ID for a single agent setup), current_project_id, current_epic_id, current_task_id, last_action, updated_at.

- (Future) Memory: Stores learned information, snippets, feedback, etc.

- (Future) FileChange: Tracks modifications to files managed by Roo Code.

### 4.2. API Endpoints
The FastAPI application will expose RESTful API endpoints for managing these entities. Key operations include:

Projects:
- POST /projects/: Create a new project.
- GET /projects/: List all projects.
- GET /projects/{project_id}: Retrieve a specific project.
- PUT /projects/{project_id}: Update a project.
- DELETE /projects/{project_id}: Delete a project.

Epics:
- POST /epics/: Create a new epic (associated with a project).
- GET /projects/{project_id}/epics/: List all epics for a given project.
- GET /epics/{epic_id}: Retrieve a specific epic.
- PUT /epics/{epic_id}: Update an epic.
- DELETE /epics/{epic_id}: Delete an epic.

Tasks:
- POST /tasks/: Create a new task (associated with an epic).
- GET /epics/{epic_id}/tasks/: List all tasks for a given epic.
- GET /tasks/{task_id}: Retrieve a specific task.
- PUT /tasks/{task_id}: Update a task.
- DELETE /tasks/{task_id}: Delete a task.

Agent State:
- GET /agent/state/: Retrieve the current agent state.
- PUT /agent/state/: Update the agent state.

Health Check:
- GET /health: A simple endpoint to verify the API is running.

## 5. Technical Design & Implementation Details
The persistence layer will be built using Python with the following key technologies:
- FastAPI: For building the web API.
- SQLAlchemy: As the Object-Relational Mapper (ORM) for database interactions.
- Pydantic: For data validation, serialization, and API schema definition.
- SQLite: As the initial database engine (file-based).
- Uvicorn: As the ASGI server to run the FastAPI application.

### 5.1. Database Schema (SQLAlchemy Models - db_models.py)
# db_models.py
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
import enum

# Define an enum for status fields
class StatusEnum(str, enum.Enum): # Inherit from str for Pydantic compatibility
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    PAUSED = "PAUSED"
    BLOCKED = "BLOCKED"
    ACTIVE = "ACTIVE" # For Projects/Epics

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    overall_goal = Column(Text, nullable=True)
    status = Column(SQLAlchemyEnum(StatusEnum), default=StatusEnum.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    epics = relationship("Epic", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status.value}')>"

class Epic(Base):
    __tablename__ = "epics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLAlchemyEnum(StatusEnum), default=StatusEnum.TODO, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="epics")
    tasks = relationship("Task", back_populates="epic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Epic(id={self.id}, name='{self.name}', project_id={self.project_id}, status='{self.status.value}')>"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    status = Column(SQLAlchemyEnum(StatusEnum), default=StatusEnum.TODO, nullable=False)
    priority = Column(Integer, default=0)
    epic_id = Column(Integer, ForeignKey("epics.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    epic = relationship("Epic", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, description='{self.description[:30]}...', epic_id={self.epic_id}, status='{self.status.value}')>"

class AgentState(Base):
    __tablename__ = "agent_states"
    # Assuming a single agent state record for simplicity, identified by id=1
    id = Column(Integer, primary_key=True, index=True, default=1)
    current_project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    current_epic_id = Column(Integer, ForeignKey("epics.id"), nullable=True)
    current_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    last_action = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships for easy loading (optional, but can be useful)
    project = relationship("Project", foreign_keys=[current_project_id])
    epic = relationship("Epic", foreign_keys=[current_epic_id])
    task = relationship("Task", foreign_keys=[current_task_id])

    def __repr__(self):
        return f"<AgentState(id={self.id}, current_task_id={self.current_task_id})>"

# TODO: Add Memory and FileChange models later

### 5.2. Database Configuration (db_config.py)
# db_config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Assuming db_models.py is in the same directory or accessible via python path
from .db_models import Base

DATABASE_URL = "sqlite:///.//roo_code_data.db"  # Database file will be roo_code_data.db

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} # Required for SQLite with FastAPI/Uvicorn
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """
    Creates all database tables defined in db_models.py that inherit from Base.
    This should be called once at application startup.
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("Database and tables created successfully (if they didn't exist).")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise

def get_db():
    """
    Dependency to get a DB session for FastAPI path operations.
    Ensures the database session is always closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### 5.3. API Data Schemas (Pydantic Models - schemas.py)
# schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
import datetime
# Assuming db_models.py is in the same directory or accessible
from .db_models import StatusEnum

# --- Task Schemas ---
class TaskBase(BaseModel):
    description: str = Field(..., min_length=1, example="Define the API endpoints for tasks.")
    priority: Optional[int] = Field(default=0, example=1)
    status: Optional[StatusEnum] = Field(default=StatusEnum.TODO, example=StatusEnum.TODO)

class TaskCreate(TaskBase):
    epic_id: int = Field(..., example=1)

class TaskUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1, example="Refine API endpoints for tasks.")
    priority: Optional[int] = Field(None, example=2)
    status: Optional[StatusEnum] = Field(None, example=StatusEnum.IN_PROGRESS)

class Task(TaskBase):
    id: int = Field(..., example=101)
    epic_id: int = Field(..., example=1)
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
        use_enum_values = True # To serialize Enum to its value

# --- Epic Schemas ---
class EpicBase(BaseModel):
    name: str = Field(..., min_length=1, example="User Authentication Feature")
    description: Optional[str] = Field(None, example="Implement all aspects of user login, registration, and management.")
    status: Optional[StatusEnum] = Field(default=StatusEnum.TODO, example=StatusEnum.TODO)

class EpicCreate(EpicBase):
    project_id: int = Field(..., example=1)

class EpicUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, example="Enhanced User Authentication")
    description: Optional[str] = Field(None, example="Implement MFA and social logins.")
    status: Optional[StatusEnum] = Field(None, example=StatusEnum.IN_PROGRESS)

class Epic(EpicBase):
    id: int = Field(..., example=21)
    project_id: int = Field(..., example=1)
    created_at: datetime.datetime
    updated_at: datetime.datetime
    tasks: List[Task] = Field(default=[], example=[])

    class Config:
        orm_mode = True
        use_enum_values = True

# --- Project Schemas ---
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, example="Roo Code Version 2.0")
    description: Optional[str] = Field(None, example="The next major release of Roo Code with enhanced features.")
    overall_goal: Optional[str] = Field(None, example="To provide a more intelligent and persistent coding assistant.")
    status: Optional[StatusEnum] = Field(default=StatusEnum.ACTIVE, example=StatusEnum.ACTIVE)

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, example="Roo Code V2 - Extended")
    description: Optional[str] = Field(None)
    overall_goal: Optional[str] = Field(None)
    status: Optional[StatusEnum] = Field(None, example=StatusEnum.PAUSED)

class Project(ProjectBase):
    id: int = Field(..., example=1)
    created_at: datetime.datetime
    updated_at: datetime.datetime
    epics: List[Epic] = Field(default=[], example=[])

    class Config:
        orm_mode = True
        use_enum_values = True

# --- AgentState Schemas ---
class AgentStateBase(BaseModel):
    current_project_id: Optional[int] = Field(None, example=1)
    current_epic_id: Optional[int] = Field(None, example=21)
    current_task_id: Optional[int] = Field(None, example=101)
    last_action: Optional[str] = Field(None, example="Generated code for user authentication module.")

class AgentStateUpdate(AgentStateBase):
    pass

class AgentStateResponse(AgentStateBase): # Renamed to avoid conflict with SQLAlchemy model name
    id: int = Field(default=1, example=1) # Assuming a single agent state with fixed ID
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
        use_enum_values = True

### 5.4. CRUD Operations Logic (db_crud.py)
# db_crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
# Assuming models and schemas are in the same directory or accessible
from . import db_models, schemas
from .db_models import StatusEnum

# --- Project CRUD ---
def create_project(db: Session, project: schemas.ProjectCreate) -> db_models.Project:
    db_project = db_models.Project(
        name=project.name,
        description=project.description,
        overall_goal=project.overall_goal,
        status=project.status if project.status else StatusEnum.ACTIVE
    )
    db.add(db_project)
    try:
        db.commit()
        db.refresh(db_project)
    except IntegrityError: # Handles unique constraint violation for name
        db.rollback()
        raise # Re-raise the exception to be handled by API layer
    return db_project

def get_project(db: Session, project_id: int) -> db_models.Project | None:
    return db.query(db_models.Project).filter(db_models.Project.id == project_id).first()

def get_project_by_name(db: Session, name: str) -> db_models.Project | None:
    return db.query(db_models.Project).filter(db_models.Project.name == name).first()

def get_all_projects(db: Session, skip: int = 0, limit: int = 100) -> list[db_models.Project]:
    return db.query(db_models.Project).offset(skip).limit(limit).all()

def update_project(db: Session, project_id: int, project_update: schemas.ProjectUpdate) -> db_models.Project | None:
    db_project = get_project(db, project_id)
    if db_project:
        update_data = project_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_project, key, value)
        try:
            db.commit()
            db.refresh(db_project)
        except IntegrityError:
            db.rollback()
            raise
    return db_project

def delete_project(db: Session, project_id: int) -> db_models.Project | None:
    db_project = get_project(db, project_id)
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project

# --- Epic CRUD ---
def create_epic(db: Session, epic: schemas.EpicCreate) -> db_models.Epic:
    db_epic = db_models.Epic(
        name=epic.name,
        description=epic.description,
        project_id=epic.project_id,
        status=epic.status if epic.status else StatusEnum.TODO
    )
    db.add(db_epic)
    db.commit()
    db.refresh(db_epic)
    return db_epic

def get_epic(db: Session, epic_id: int) -> db_models.Epic | None:
    return db.query(db_models.Epic).filter(db_models.Epic.id == epic_id).first()

def get_epics_for_project(db: Session, project_id: int, skip: int = 0, limit: int = 100) -> list[db_models.Epic]:
    return db.query(db_models.Epic).filter(db_models.Epic.project_id == project_id).offset(skip).limit(limit).all()

def update_epic(db: Session, epic_id: int, epic_update: schemas.EpicUpdate) -> db_models.Epic | None:
    db_epic = get_epic(db, epic_id)
    if db_epic:
        update_data = epic_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_epic, key, value)
        db.commit()
        db.refresh(db_epic)
    return db_epic

def delete_epic(db: Session, epic_id: int) -> db_models.Epic | None:
    db_epic = get_epic(db, epic_id)
    if db_epic:
        db.delete(db_epic)
        db.commit()
    return db_epic

# --- Task CRUD ---
def create_task(db: Session, task: schemas.TaskCreate) -> db_models.Task:
    db_task = db_models.Task(
        description=task.description,
        epic_id=task.epic_id,
        priority=task.priority,
        status=task.status if task.status else StatusEnum.TODO
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int) -> db_models.Task | None:
    return db.query(db_models.Task).filter(db_models.Task.id == task_id).first()

def get_tasks_for_epic(db: Session, epic_id: int, skip: int = 0, limit: int = 100) -> list[db_models.Task]:
    return db.query(db_models.Task).filter(db_models.Task.epic_id == epic_id).order_by(db_models.Task.priority.desc(), db_models.Task.created_at).offset(skip).limit(limit).all()

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate) -> db_models.Task | None:
    db_task = get_task(db, task_id)
    if db_task:
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int) -> db_models.Task | None:
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

# --- AgentState CRUD ---
AGENT_STATE_DEFAULT_ID = 1 # Assuming a single agent state record

def get_agent_state(db: Session) -> db_models.AgentState | None:
    return db.query(db_models.AgentState).filter(db_models.AgentState.id == AGENT_STATE_DEFAULT_ID).first()

def upsert_agent_state(db: Session, agent_state_update: schemas.AgentStateUpdate) -> db_models.AgentState:
    db_state = get_agent_state(db)
    update_data = agent_state_update.model_dump(exclude_unset=True)

    if not db_state:
        # Create new state with default ID and provided updates
        db_state = db_models.AgentState(id=AGENT_STATE_DEFAULT_ID, **update_data)
        db.add(db_state)
    else:
        # Update existing state
        for key, value in update_data.items():
            setattr(db_state, key, value)
    db.commit()
    db.refresh(db_state)
    return db_state

### 5.5. FastAPI Application (main.py)
# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

# Assuming your files are structured like:
# your_project/
# ├── app/  <-- Your main application package
# │   ├── main.py
# │   ├── db_models.py
# │   ├── db_config.py
# │   ├── db_crud.py
# │   ├── schemas.py
# To run with uvicorn from outside 'app': uvicorn app.main:app
# If main.py is at the root of your project, adjust imports.
# For this example, assuming main.py is inside an 'app' directory:
from . import db_config, db_crud, schemas # Use relative imports if main.py is part of a package

# Create database tables if they don't exist
# This is a simple way for development. For production, use Alembic migrations.
try:
    db_config.create_db_and_tables()
except Exception as e:
    print(f"Could not create database tables. Error: {e}")
    # Depending on your setup, you might want to exit or log this more formally.


app = FastAPI(
    title="Roo Code Data API",
    version="1.0.0",
    description="API for managing Roo Code projects, epics, tasks, and agent state.",
    # You can add more metadata like contact, license_info, etc.
)

# --- API Endpoints ---

# Helper for DB session
def get_db():
    return db_config.get_db() # This is already a generator

# Projects
@app.post("/projects/", response_model=schemas.Project, status_code=status.HTTP_201_CREATED, tags=["Projects"], summary="Create a new project")
def create_new_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    try:
        return db_crud.create_project(db=db, project=project)
    except IntegrityError: # Catches unique constraint violation for project name
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Project with name '{project.name}' already exists.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")


@app.get("/projects/", response_model=List[schemas.Project], tags=["Projects"], summary="List all projects")
def read_all_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = db_crud.get_all_projects(db, skip=skip, limit=limit)
    return projects

@app.get("/projects/{project_id}", response_model=schemas.Project, tags=["Projects"], summary="Get a specific project by ID")
def read_single_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db_crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return db_project

@app.put("/projects/{project_id}", response_model=schemas.Project, tags=["Projects"], summary="Update an existing project")
def update_existing_project(project_id: int, project_update: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    try:
        db_project = db_crud.update_project(db, project_id=project_id, project_update=project_update)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Project name conflict during update.")
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return db_project

@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Projects"], summary="Delete a project")
def delete_existing_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db_crud.delete_project(db, project_id=project_id)
    if db_project is None: # delete_project returns the deleted object or None
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return # Return No Content for successful deletion


# Epics
@app.post("/epics/", response_model=schemas.Epic, status_code=status.HTTP_201_CREATED, tags=["Epics"], summary="Create a new epic")
def create_new_epic(epic: schemas.EpicCreate, db: Session = Depends(get_db)):
    db_project = db_crud.get_project(db, project_id=epic.project_id)
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {epic.project_id} not found. Cannot create epic.")
    return db_crud.create_epic(db=db, epic=epic)

@app.get("/projects/{project_id}/epics/", response_model=List[schemas.Epic], tags=["Epics"], summary="List epics for a project")
def read_epics_for_project(project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_project = db_crud.get_project(db, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {project_id} not found.")
    return db_crud.get_epics_for_project(db, project_id=project_id, skip=skip, limit=limit)

@app.get("/epics/{epic_id}", response_model=schemas.Epic, tags=["Epics"], summary="Get a specific epic by ID")
def read_single_epic(epic_id: int, db: Session = Depends(get_db)):
    db_epic = db_crud.get_epic(db, epic_id=epic_id)
    if db_epic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Epic not found")
    return db_epic

@app.put("/epics/{epic_id}", response_model=schemas.Epic, tags=["Epics"], summary="Update an existing epic")
def update_existing_epic(epic_id: int, epic_update: schemas.EpicUpdate, db: Session = Depends(get_db)):
    db_epic = db_crud.update_epic(db, epic_id=epic_id, epic_update=epic_update)
    if db_epic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Epic not found")
    return db_epic

@app.delete("/epics/{epic_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Epics"], summary="Delete an epic")
def delete_existing_epic(epic_id: int, db: Session = Depends(get_db)):
    db_epic = db_crud.delete_epic(db, epic_id=epic_id)
    if db_epic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Epic not found")
    return


# Tasks
@app.post("/tasks/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"], summary="Create a new task")
def create_new_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_epic = db_crud.get_epic(db, epic_id=task.epic_id)
    if not db_epic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Epic with id {task.epic_id} not found. Cannot create task.")
    return db_crud.create_task(db=db, task=task)

@app.get("/epics/{epic_id}/tasks/", response_model=List[schemas.Task], tags=["Tasks"], summary="List tasks for an epic")
def read_tasks_for_epic(epic_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_epic = db_crud.get_epic(db, epic_id=epic_id)
    if not db_epic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Epic with id {epic_id} not found.")
    return db_crud.get_tasks_for_epic(db, epic_id=epic_id, skip=skip, limit=limit)

@app.get("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"], summary="Get a specific task by ID")
def read_single_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db_crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task

@app.put("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"], summary="Update an existing task")
def update_existing_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = db_crud.update_task(db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return