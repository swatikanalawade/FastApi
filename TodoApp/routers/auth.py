from fastapi import APIRouter, Depends, status, HTTPException
from datetime import timedelta, datetime
from database import SessionLocal
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

router = APIRouter(
    prefix="/auth",
    tags = ["auth"]
)

SECRET_KEY = "Uijt2345jt6789bo9788fybnqmf"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

bcrypt_context = CryptContext(schemes=['bcrypt'])

def authenticate_user(username: str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

class CreateUserRequest(BaseModel):
    email : str 
    username : str
    first_name : str
    last_name : str
    password : str
    role : str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
def create_user(db:db_dependency, user_request:CreateUserRequest):
    user_model = Users(
            email = user_request.email,
            username = user_request.username,
            first_name = user_request.first_name,
            last_name = user_request.last_name,
            hashed_password = bcrypt_context.hash(user_request.password),
            role = user_request.role,
            is_active = True
            )
    db.add(user_model)
    db.commit()

def create_access_token(username:str, user_id: int, expire_date=timedelta()):
    encode = {"sub":username, "id": user_id}
    expires = datetime.utcnow() + expire_date
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
                           db:db_dependency):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user.")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(db:db_dependency, username, password):                      
    user = db.query(Users).filter(Users.username == username).first()
    if user:
        password = bcrypt_context.verify(password, user.hashed_password)     
        return {"username":username, "id":user.id}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user")
    