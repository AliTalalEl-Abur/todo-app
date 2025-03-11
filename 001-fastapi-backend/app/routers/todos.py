from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import ToDo
from app import schemas
from app import crud

router = APIRouter(prefix="/todos", tags=["todos"])  # Prefijo y etiqueta

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ToDoResponse)
def create_todo(todo: schemas.ToDoRequest, db: Session = Depends(get_db)):
    db_todo = crud.create_todo(db, todo)
    return db_todo

@router.get("", response_model=list[schemas.ToDoResponse])  # Path vacío, pero el prefijo lo completa
def get_todos(completed: bool = None, db: Session = Depends(get_db)):
    todos = crud.read_todos(db, completed)
    return todos

@router.get("/{id}", response_model=schemas.ToDoResponse)
def get_todo_by_id(id: int, db: Session = Depends(get_db)):
    todo = crud.read_todo(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{id}", response_model=schemas.ToDoResponse)
def update_todo(id: int, todo: schemas.ToDoRequest, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, id, todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_todo(id: int, db: Session = Depends(get_db)):
    res = crud.delete_todo(db, id)
    if res is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}