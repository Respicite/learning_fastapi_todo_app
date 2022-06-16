import sys
sys.path.append("..")
import models
from database import engine, SessionLocal

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional
from .auth import get_current_user, get_user_exception


router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404:  {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)


class ToDo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="Priority must be between 1 and 5")
    complete: bool


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close


def item_not_found():
    return HTTPException(status_code=404, detail="Item not found")


def transaction_successful(status_code: int):
    return {
        'status': status_code,
        'transaction': 'successful'
    }


@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@router.get("/user")
async def read_user_todos(user: dict = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()


@router.get("/{todo_id}")
async def read_todo(todo_id: int,
                    user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    todo_model = db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .filter(models.Todos.owner_id == user.get("id")) \
        .first()

    if todo_model is not None:
        return todo_model
    raise item_not_found()


@router.post("/")
async def create_todo(todo: ToDo, db: Session = Depends(get_db),
                      user: dict = Depends(get_current_user)):
    if user is None:
        raise get_user_exception()

    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get("id")

    db.add(todo_model)
    db.commit()

    return transaction_successful(201)


@router.put("/{todo_id}")
async def update_todo(todo_id: int, todo: ToDo, db: Session = Depends(get_db),
                      user: dict = Depends(get_current_user)):
    if user is None:
        raise get_user_exception()

    todo_model = db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .filter(models.Todos.owner_id == user.get("id")) \
        .first()

    if todo_model is None:
        raise item_not_found()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    db.add(todo_model)
    db.commit()

    return transaction_successful(200)


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db),
                      user: dict = Depends(get_current_user)):
    if user is None:
        raise get_user_exception()

    todo_model = db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .filter(models.Todos.owner_id == user.get("id")) \
        .first()

    if todo_model is None:
        raise item_not_found()

    db.delete(todo_model)
    db.commit()

    return transaction_successful(204)
