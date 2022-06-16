import sys
sys.path.append("..")
import models
from database import engine, SessionLocal

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from .auth import get_current_user, get_user_exception, verify_password, get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"User": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


def user_not_found():
    return HTTPException(status_code=404, detail="User not found")


@router.get("/")
async def read_all(user_id: Optional[str] = None, db: Session = Depends(get_db)):
    if user_id is None:
        return db.query(models.Users).all()

    user_model = db.query(models.Users) \
        .filter(models.Users.id == user_id) \
        .first()

    if user_model is not None:
        return user_model

    raise user_not_found()


@router.get("/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.Users) \
        .filter(models.Users.id == user_id) \
        .first()

    if user_model is not None:
        return user_model

    raise user_not_found()


@router.put("/change_password")
async def change_password(user_verification: UserVerification, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

    if user_model is not None:
        if user_verification.username == user_model.username and verify_password(user_verification.password, user_model.hashed_password):
            user_model.hashed_password = get_password_hash(user_verification.new_password)
            db.add(user_model)
            db.commit()

            return {
                'status': 200,
                'transaction': 'successful'
            }

    raise user_not_found()


@router.delete("/delete_user")
async def delete_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

    if user_model is not None:
        db.delete(user_model)
        db.commit()

        return {
            'status': 203,
            'transaction': 'successful'
        }

    raise user_not_found()
