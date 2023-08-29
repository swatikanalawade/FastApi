from fastapi import APIRouter, Depends, HTTPException, status, Path
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
from pydantic import BaseModel, Field
from routers import auth
from .auth import get_current_user

router = APIRouter()

router.include_router(auth.router)

class TodoRequest(BaseModel):
    title : str = Field(min_length=3)
    description : str = Field(min_length=3, max_length=100)
    priority : int = Field(gt=0, lt=6)
    complete : bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/")
def read_all(db: db_dependency ):
    return db.query(Todos).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK )
def read_todo(db: db_dependency, todo_id:int = Path(gt=0)):
    model = db.query(Todos).filter(Todos.id == todo_id).first()
    if model:
        return model
    return HTTPException(status_code=404, detail="Todo Not Found")

@router.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(user:user_dependency,
                db:db_dependency,todo_request: TodoRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    todo_model =Todos(**todo_request.model_dump(),owner_id = user.get("id") )
    db.add(todo_model)
    db.commit()

@router.put("/todo/{todo_id}", status_code= status.HTTP_204_NO_CONTENT)
def update_todo(db:db_dependency,todo_request:TodoRequest,todo_id :int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model == None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    todo_model.title = todo_request.title
    todo_model.complete = todo_request.complete
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    db.add(todo_model)
    db.commit()
         
@router.delete("/todo/{todo_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_todo(db:db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit() 