from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(
    prefix="/memory_entries",
    tags=["memory_entries"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.MemoryEntryRead, status_code=status.HTTP_201_CREATED)
def create_memory_entry(memory_entry: schemas.MemoryEntryCreate, db: Session = Depends(get_db)):
    return crud.create_memory_entry(db=db, memory_entry=memory_entry)


@router.get("/{memory_entry_id}", response_model=schemas.MemoryEntryRead)
def read_memory_entry(memory_entry_id: int, db: Session = Depends(get_db)):
    db_memory_entry = crud.get_memory_entry(db=db, memory_entry_id=memory_entry_id)
    if db_memory_entry is None:
        raise HTTPException(status_code=404, detail="MemoryEntry not found")
    return db_memory_entry


@router.get("/", response_model=List[schemas.MemoryEntryRead])
def read_memory_entries(
    skip: int = 0,
    limit: int = 100,
    roomode_id: Optional[int] = None,
    type: Optional[str] = None,
    related_task_id: Optional[int] = None,
    related_project_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    memory_entries, total = crud.get_memory_entries(
        db,
        skip=skip,
        limit=limit,
        roomode_id=roomode_id,
        type=type,
        related_task_id=related_task_id,
        related_project_id=related_project_id,
    )
    return memory_entries


@router.patch("/{memory_entry_id}", response_model=schemas.MemoryEntryRead)
def update_memory_entry(
    memory_entry_id: int,
    memory_entry: schemas.MemoryEntryUpdate,
    db: Session = Depends(get_db)
):
    db_memory_entry = crud.update_memory_entry(db=db, memory_entry_id=memory_entry_id, memory_entry_update=memory_entry)
    if db_memory_entry is None:
        raise HTTPException(status_code=404, detail="MemoryEntry not found")
    return db_memory_entry


@router.delete("/{memory_entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_memory_entry(memory_entry_id: int, db: Session = Depends(get_db)):
    if not crud.delete_memory_entry(db=db, memory_entry_id=memory_entry_id):
        raise HTTPException(status_code=404, detail="MemoryEntry not found")
    return {"ok": True}