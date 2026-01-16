"""
Epic management API endpoints.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.database import get_db

router = APIRouter(prefix="/epics", tags=["epics"])


@router.post("/", response_model=schemas.EpicRead, status_code=status.HTTP_201_CREATED)
def create_epic(
    epic: schemas.EpicCreate,
    db: Session = Depends(get_db)
) -> schemas.EpicRead:
    """
    Create a new epic.
    
    Args:
        epic: Epic data to create
        db: Database session
        
    Returns:
        Created epic data
        
    Raises:
        HTTPException: If associated project not found
    """
    # Verify project exists
    project = crud.get_project(db=db, project_id=epic.project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {epic.project_id} not found"
        )
    
    return crud.create_epic(db=db, epic=epic)


@router.get("/", response_model=schemas.PaginatedEpicsResponse)
def list_epics(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    project_id: Optional[int] = Query(default=None, description="Filter by project ID"),
    status: Optional[models.EpicStatus] = Query(default=None, description="Filter by epic status"),
    db: Session = Depends(get_db)
) -> schemas.PaginatedEpicsResponse:
    """
    List epics with pagination and optional filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        project_id: Optional project ID filter
        status: Optional status filter
        db: Database session
        
    Returns:
        Paginated list of epics
    """
    epics, total = crud.get_epics(
        db=db, 
        skip=skip, 
        limit=limit, 
        project_id=project_id, 
        status=status
    )
    
    return schemas.PaginatedEpicsResponse(
        items=epics,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{epic_id}", response_model=schemas.EpicRead)
def get_epic(
    epic_id: int,
    db: Session = Depends(get_db)
) -> schemas.EpicRead:
    """
    Get a specific epic by ID.
    
    Args:
        epic_id: Epic ID
        db: Database session
        
    Returns:
        Epic data
        
    Raises:
        HTTPException: If epic not found
    """
    epic = crud.get_epic(db=db, epic_id=epic_id)
    if not epic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Epic with id {epic_id} not found"
        )
    return epic


@router.get("/{epic_id}/with-tasks", response_model=schemas.EpicReadWithTasks)
def get_epic_with_tasks(
    epic_id: int,
    db: Session = Depends(get_db)
) -> schemas.EpicReadWithTasks:
    """
    Get a specific epic by ID with its associated tasks.
    
    Args:
        epic_id: Epic ID
        db: Database session
        
    Returns:
        Epic data with tasks
        
    Raises:
        HTTPException: If epic not found
    """
    epic = crud.get_epic(db=db, epic_id=epic_id)
    if not epic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Epic with id {epic_id} not found"
        )
    return epic


@router.put("/{epic_id}", response_model=schemas.EpicRead)
def update_epic(
    epic_id: int,
    epic_update: schemas.EpicUpdate,
    db: Session = Depends(get_db)
) -> schemas.EpicRead:
    """
    Update a specific epic.
    
    Args:
        epic_id: Epic ID
        epic_update: Epic update data
        db: Database session
        
    Returns:
        Updated epic data
        
    Raises:
        HTTPException: If epic not found or project not found
    """
    # If updating project_id, verify the new project exists
    if epic_update.project_id is not None:
        project = crud.get_project(db=db, project_id=epic_update.project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {epic_update.project_id} not found"
            )
    
    epic = crud.update_epic(db=db, epic_id=epic_id, epic_update=epic_update)
    if not epic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Epic with id {epic_id} not found"
        )
    return epic


@router.delete("/{epic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_epic(
    epic_id: int,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a specific epic.
    
    Args:
        epic_id: Epic ID
        db: Database session
        
    Raises:
        HTTPException: If epic not found
    """
    success = crud.delete_epic(db=db, epic_id=epic_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Epic with id {epic_id} not found"
        )
