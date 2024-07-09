from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Path
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Todos
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(prefix='/admin',
    tags=['admin']

)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/admin", status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency, user:user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail="Authencation Failed")
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todos(db:db_dependency, user:user_dependency, todo_id:int=Path(gt=0)):
    print("user-->", user)
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authencation Failed')
    print("todo_id-->", todo_id)
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    print(todo_model)
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
