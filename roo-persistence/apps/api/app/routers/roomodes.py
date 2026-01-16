from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(
    prefix="/roomodes",
    tags=["roomodes"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.RoomodeRead, status_code=status.HTTP_201_CREATED)
def create_roomode(roomode: schemas.RoomodeCreate, db: Session = Depends(get_db)):
    return crud.create_roomode(db=db, roomode=roomode)


@router.get("/{roomode_id}", response_model=schemas.RoomodeRead)
def read_roomode(roomode_id: int, db: Session = Depends(get_db)):
    db_roomode = crud.get_roomode(db=db, roomode_id=roomode_id)
    if db_roomode is None:
        raise HTTPException(status_code=404, detail="Roomode not found")
    return db_roomode


@router.get("/", response_model=List[schemas.RoomodeRead])
def read_roomodes(
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    roomodes, total = crud.get_roomodes(db, skip=skip, limit=limit, type=type, is_active=is_active)
    return roomodes


@router.patch("/{roomode_id}", response_model=schemas.RoomodeRead)
def update_roomode(
    roomode_id: int,
    roomode: schemas.RoomodeUpdate,
    db: Session = Depends(get_db)
):
    db_roomode = crud.update_roomode(db=db, roomode_id=roomode_id, roomode_update=roomode)
    if db_roomode is None:
        raise HTTPException(status_code=404, detail="Roomode not found")
    return db_roomode


@router.delete("/{roomode_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_roomode(roomode_id: int, db: Session = Depends(get_db)):
    if not crud.delete_roomode(db=db, roomode_id=roomode_id):
        raise HTTPException(status_code=404, detail="Roomode not found")
    return {"ok": True}