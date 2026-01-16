"""
Agent state management API endpoints.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/agent-states", tags=["agent-states"])


@router.post("/", response_model=schemas.AgentStateRead, status_code=status.HTTP_201_CREATED)
def create_agent_state(
    agent_state: schemas.AgentStateCreate,
    db: Session = Depends(get_db)
) -> schemas.AgentStateRead:
    """
    Create a new agent state.
    
    Args:
        agent_state: Agent state data to create
        db: Database session
        
    Returns:
        Created agent state data
        
    Raises:
        HTTPException: If agent_id already exists
    """
    # Check if agent state already exists
    existing_state = crud.get_agent_state(db=db, agent_id=agent_state.agent_id)
    if existing_state:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Agent state for agent_id '{agent_state.agent_id}' already exists"
        )
    
    # Verify referenced entities exist
    if agent_state.current_task_id:
        task = crud.get_task(db=db, task_id=agent_state.current_task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {agent_state.current_task_id} not found"
            )
    
    if agent_state.current_project_id:
        project = crud.get_project(db=db, project_id=agent_state.current_project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {agent_state.current_project_id} not found"
            )
    
    return crud.create_agent_state(db=db, agent_state=agent_state)


@router.get("/", response_model=list[schemas.AgentStateRead])
def list_agent_states(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    is_active: Optional[bool] = Query(default=None, description="Filter by active status"),
    db: Session = Depends(get_db)
) -> list[schemas.AgentStateRead]:
    """
    List agent states with pagination and optional filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        is_active: Optional active status filter
        db: Database session
        
    Returns:
        List of agent states
    """
    agent_states, _ = crud.get_agent_states(
        db=db,
        skip=skip,
        limit=limit,
        is_active=is_active
    )
    
    return agent_states


@router.get("/{agent_id}", response_model=schemas.AgentStateRead)
def get_agent_state(
    agent_id: str,
    db: Session = Depends(get_db)
) -> schemas.AgentStateRead:
    """
    Get agent state by agent ID.
    
    Args:
        agent_id: Agent ID
        db: Database session
        
    Returns:
        Agent state data
        
    Raises:
        HTTPException: If agent state not found
    """
    agent_state = crud.get_agent_state(db=db, agent_id=agent_id)
    if not agent_state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent state for agent_id '{agent_id}' not found"
        )
    return agent_state


@router.put("/{agent_id}", response_model=schemas.AgentStateRead)
def update_agent_state(
    agent_id: str,
    agent_state_update: schemas.AgentStateUpdate,
    db: Session = Depends(get_db)
) -> schemas.AgentStateRead:
    """
    Update agent state.
    
    Args:
        agent_id: Agent ID
        agent_state_update: Agent state update data
        db: Database session
        
    Returns:
        Updated agent state data
        
    Raises:
        HTTPException: If agent state not found or referenced entities not found
    """
    # Verify referenced entities exist
    if agent_state_update.current_task_id is not None:
        task = crud.get_task(db=db, task_id=agent_state_update.current_task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {agent_state_update.current_task_id} not found"
            )
    
    if agent_state_update.current_project_id is not None:
        project = crud.get_project(db=db, project_id=agent_state_update.current_project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {agent_state_update.current_project_id} not found"
            )
    
    agent_state = crud.update_agent_state(
        db=db,
        agent_id=agent_id,
        agent_state_update=agent_state_update
    )
    if not agent_state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent state for agent_id '{agent_id}' not found"
        )
    return agent_state


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent_state(
    agent_id: str,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete agent state.
    
    Args:
        agent_id: Agent ID
        db: Database session
        
    Raises:
        HTTPException: If agent state not found
    """
    success = crud.delete_agent_state(db=db, agent_id=agent_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent state for agent_id '{agent_id}' not found"
        )


@router.patch("/{agent_id}/activity", response_model=schemas.AgentStateRead)
def update_agent_activity(
    agent_id: str,
    db: Session = Depends(get_db)
) -> schemas.AgentStateRead:
    """
    Update agent's last activity timestamp to current time.
    
    Args:
        agent_id: Agent ID
        db: Database session
        
    Returns:
        Updated agent state data
        
    Raises:
        HTTPException: If agent state not found
    """
    # This will automatically update last_activity in the CRUD function
    agent_state_update = schemas.AgentStateUpdate()
    agent_state = crud.update_agent_state(
        db=db,
        agent_id=agent_id,
        agent_state_update=agent_state_update
    )
    if not agent_state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent state for agent_id '{agent_id}' not found"
        )
    return agent_state
