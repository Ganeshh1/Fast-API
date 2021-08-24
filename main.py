import sqlalchemy
import databases
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

class Todo(BaseModel):

    name: str
    due_date: str
    description: str

app = FastAPI()

# Create, Read, Update, Delete

store_todo = []
metadata = sqlalchemy.MetaData()
DATABASE_URI ="mysql://root:GaneshKumar06061999@localhost/fastapi"

database = databases.Database(DATABASE_URI)

register = sqlalchemy.Table(
    "register",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(500)),
    sqlalchemy.Column("date_created", sqlalchemy.DateTime())
)

engine = sqlalchemy.create_engine(
    DATABASE_URI, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)


@app.get('/')
async def home():
    return {"Hello": "World"}

@app.post('/todo/')
async def create_todo(todo: Todo):
    store_todo.append(todo)
    return todo

@app.get('/todo/', response_model=List[Todo])
async def get_all_todos():
    return store_todo

@app.get('/todo/{id}')
async def get_todo(id: int):

    try:
        
        return store_todo[id-1]
    
    except:
        
        raise HTTPException(status_code=404, detail="Todo Not Found")

@app.put('/todo/{id}')
async def update_todo(id: int, todo: Todo):

    try:

        store_todo[id-1] = todo
        return store_todo[id-1]
    
    except:
        
        raise HTTPException(status_code=404, detail="Todo Not Found")

@app.delete('/todo/{id}')
async def delete_todo(id: int):

    try:

        obj = store_todo[id-1]
        store_todo.pop(id-1)
        return obj
    
    except:
        
        raise HTTPException(status_code=404, detail="Todo Not Found")

