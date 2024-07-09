from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Todos
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(max_length=500)
    description: str = Field(min_length=10)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=True)


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authorized')
    db_model = db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()
    return db_model


@router.get("/todo/", status_code=status.HTTP_200_OK)
async def read_todo(user:user_dependency, db: db_dependency, todo_id):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authorized')
    todo_models = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_models is None:
        raise HTTPException(404, detail=' ID not found')
    return todo_models


@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authorized')
    todo_model = Todos(**todo_request.dict(), owner_id=user.get('user_id'))
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user:user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not authorized')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id).first()
    if todo_model is None:
        raise HTTPException(404, detail='Id not found')
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    db.add(todo_model)
    db.commit()
