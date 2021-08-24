from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')

# Dependency

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()

#OAuth2.0 Auth
@app.post('/token')
async def token(form_data : OAuth2PasswordRequestForm = Depends()):
    return {'access_token' : form_data.username +'Token'}

@app.get('/')
async def index(token : str = Depends(oauth2_scheme)):
    return {'token' : token}

#Performing Crud Operations

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db),token : str = Depends(oauth2_scheme)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users( db: Session = Depends(get_db),token : str = Depends(oauth2_scheme)):
    users = crud.get_users(db)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db),token : str = Depends(oauth2_scheme)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Profile)
def create_item_for_user(
    user_id: int, item: schemas.ProfileCreate, db: Session = Depends(get_db),
    token : str = Depends(oauth2_scheme)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Profile])
def read_items(db: Session = Depends(get_db),token : str = Depends(oauth2_scheme)):
    items = crud.get_items(db)
    return items

@app.delete('/delete/{user_id}',response_model=schemas.User)
def delete_user(user_id:int , db:Session = Depends(get_db),token:str=Depends(oauth2_scheme)):
    db_user = crud.delete_user(db,user_id = user_id)
    if db_user is None:
        raise HTTPException(status_code=404,detail = "User Not Found")
    return db_user

@app.delete("/users/items/delete", response_model=schemas.Profile)
def delete_item(
    item_id: int, item: schemas.ProfileCreate, db: Session = Depends(get_db),
    token : str = Depends(oauth2_scheme)
):
    return crud.delete_user_item(db=db, item=item, item_id=item_id)