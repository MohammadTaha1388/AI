from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database.db import SessionLocal, engine
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin

from app.database.db import Base

Base.metadata.create_all(bind=engine)

router = APIRouter()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    hashed_password = pwd_context.hash(
        user.password
    )

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created",
        "id": new_user.id
    }


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not pwd_context.verify(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )

    return {
        "message": "Login successful",
        "user": db_user.username
    }
