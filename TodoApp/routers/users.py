from fastapi import APIRouter, HTTPException, Depends, status
from .auth import create_access_token, get_current_user
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import Todos, Users
from database import SessionLocal
from pydantic import BaseModel, Field

router = APIRouter(tags=['users'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserVerification(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6)


@router.get('/users', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency, user: user_dependency):
    print(user)
    if user is None:
        raise HTTPException(status_code=404, detail="Not Authorized")
    return db.query(Users).filter(Users.id == user.get('user_id')).first()


@router.put('/change_password', status_code=status.HTTP_200_OK)
async def update_password(db: db_dependency, user: user_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    user_model = db.query(Users).filter(Users.id == user.get('user_id')).first()
    if not bcrypt_context.verify(user_verification.current_password, user_model.hashed_password):
        raise HTTPException(status_code=404, detail='Error on Password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put('/update/{phone_number}', status_code=status.HTTP_201_CREATED)
async def update_hone_number(db:db_dependency, user:user_dependency, phone_number:str):
    if user is None:
        raise HTTPException(status_code=404, detail='User not authorized')
    user_model = db.query(Users).filter(Users.id == user.get('user_id')).first()
    if phone_number is None:
        raise HTTPException(status_code=404, detail='Phone number is not valid')

    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
