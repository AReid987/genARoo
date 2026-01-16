"""
Task management API endpoints.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)
) -> schemas.TaskRead:
    """
    Create a new task.
    
    Args:
        task: Task data to create
        db: Database session
        
    Returns:
        Created task data
        
    Raises:
        HTTPException: If associated epic not found
    """
    # Verify epic exists
    epic = crud.get_epic(db=db, epic_id=task.epic_id)
    if not epic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Epic with id {task.epic_id} not found"
        )
    
    return crud.create_task(db=db, task=task)


@router.get("/", response_model=schemas.PaginatedTasksResponse)
def list_tasks(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    epic_id: Optional[int] = Query(default=None, description="Filter by epic ID"),
    status: Optional[models.TaskStatus] = Query(default=None, description="Filter by task status"),
    priority: Optional[models.TaskPriority] = Query(default=None, description="Filter by task priority"),
    assignee: Optional[str] = Query(default=None, description="Filter by assignee"),
    db: Session = Depends(get_db)
) -> schemas.PaginatedTasksResponse:
    """
    List tasks with pagination and optional filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        epic_id: Optional epic ID filter
        status: Optional status filter
        priority: Optional priority filter
        assignee: Optional assignee filter
        db: Database session
        
    Returns:
        Paginated list of tasks
    """
    tasks, total = crud.get_tasks(
        db=db,
        skip=skip,
        limit=limit,
        epic_id=epic_id,
        status=status,
        priority=priority,
        assignee=assignee
    )
    
    return schemas.PaginatedTasksResponse(
        items=tasks,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{task_id}", response_model=schemas.TaskRead)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
) -> schemas.TaskRead:
    """
    Get a specific task by ID.
    
    Args:
        task_id: Task ID
        db: Database session
        
    Returns:
        Task data
        
    Raises:
        HTTPException: If task not found
    """
    task = crud.get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.put("/{task_id}", response_model=schemas.TaskRead)
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db)
) -> schemas.TaskRead:
    """
    Update a specific task.
    
    Args:
        task_id: Task ID
        task_update: Task update data
        db: Database session
        
    Returns:
        Updated task data
        
    Raises:
        HTTPException: If task not found or epic not found
    """
    # If updating epic_id, verify the new epic exists
    if task_update.epic_id is not None:
        epic = crud.get_epic(db=db, epic_id=task_update.epic_id)
        if not epic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Epic with id {task_update.epic_id} not found"
            )
    
    task = crud.update_task(db=db, task_id=task_id, task_update=task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a specific task.
    
    Args:
        task_id: Task ID
        db: Database session
        
    Raises:
        HTTPException: If task not found
    """
    success = crud.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )


@router.patch("/{task_id}/status", response_model=schemas.TaskRead)
def update_task_status(
    task_id: int,
    status: models.TaskStatus,
    db: Session = Depends(get_db)
) -> schemas.TaskRead:
    """
    Update only the status of a specific task.
    
    Args:
        task_id: Task ID
        status: New task status
        db: Database session
        
    Returns:
        Updated task data
        
    Raises:
        HTTPException: If task not found
    """
    task_update = schemas.TaskUpdate(status=status)
    task = crud.update_task(db=db, task_id=task_id, task_update=task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.patch("/{task_id}/assignee", response_model=schemas.TaskRead)
def update_task_assignee(
    task_id: int,
    assignee: Optional[str],
    db: Session = Depends(get_db)
) -> schemas.TaskRead:
    """
    Update only the assignee of a specific task.
    
    Args:
        task_id: Task ID
        assignee: New task assignee (or None to unassign)
        db: Database session
        
    Returns:
        Updated task data
        
    Raises:
        HTTPException: If task not found
    """
    task_update = schemas.TaskUpdate(assignee=assignee)
    task = crud.update_task(db=db, task_id=task_id, task_update=task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task
