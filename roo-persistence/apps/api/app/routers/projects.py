"""
Project management API endpoints.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.database import get_db

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db)
) -> schemas.ProjectRead:
    """
    Create a new project.
    
    Args:
        project: Project data to create
        db: Database session
        
    Returns:
        Created project data
    """
    return crud.create_project(db=db, project=project)


@router.get("/", response_model=schemas.PaginatedProjectsResponse)
def list_projects(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    status: Optional[models.ProjectStatus] = Query(default=None, description="Filter by project status"),
    db: Session = Depends(get_db)
) -> schemas.PaginatedProjectsResponse:
    """
    List projects with pagination and optional filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        status: Optional status filter
        db: Database session
        
    Returns:
        Paginated list of projects
    """
    projects, total = crud.get_projects(db=db, skip=skip, limit=limit, status=status)
    
    return schemas.PaginatedProjectsResponse(
        items=projects,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{project_id}", response_model=schemas.ProjectRead)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
) -> schemas.ProjectRead:
    """
    Get a specific project by ID.
    
    Args:
        project_id: Project ID
        db: Database session
        
    Returns:
        Project data
        
    Raises:
        HTTPException: If project not found
    """
    project = crud.get_project(db=db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    return project


@router.get("/{project_id}/with-epics", response_model=schemas.ProjectReadWithEpics)
def get_project_with_epics(
    project_id: int,
    db: Session = Depends(get_db)
) -> schemas.ProjectReadWithEpics:
    """
    Get a specific project by ID with its associated epics.
    
    Args:
        project_id: Project ID
        db: Database session
        
    Returns:
        Project data with epics
        
    Raises:
        HTTPException: If project not found
    """
    project = crud.get_project(db=db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    return project


@router.put("/{project_id}", response_model=schemas.ProjectRead)
def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    db: Session = Depends(get_db)
) -> schemas.ProjectRead:
    """
    Update a specific project.
    
    Args:
        project_id: Project ID
        project_update: Project update data
        db: Database session
        
    Returns:
        Updated project data
        
    Raises:
        HTTPException: If project not found
    """
    project = crud.update_project(db=db, project_id=project_id, project_update=project_update)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a specific project.
    
    Args:
        project_id: Project ID
        db: Database session
        
    Raises:
        HTTPException: If project not found
    """
    success = crud.delete_project(db=db, project_id=project_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
