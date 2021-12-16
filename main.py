import datetime, uuid

from typing import List

import databases

import sqlalchemy

from models.users_model import UserList, UserEntry, UserUpdate, UserDelete
from models.group_model import GroupList, GroupEntry, GroupUpdate, GroupDelete

from passlib.context import CryptContext
from fastapi import FastAPI
from pydantic import BaseModel


DATABASE_URL = "postgresql://kxcmhbkhvyyfel:bcea7a52633f6d2b8278c4880343774c2166835491d099bc28e3300e7d1ca5ba@ec2-52-213-119-221.eu-west-1.compute.amazonaws.com:5432/d7c6o4a367jfbo"

database = databases.Database(DATABASE_URL)


metadata = sqlalchemy.MetaData()




users = sqlalchemy.Table(
    "py_users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("gender", sqlalchemy.CHAR  ),
    sqlalchemy.Column("create_at", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.CHAR  ),
)

groups = sqlalchemy.Table(
    "group",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="Fart-API postgreSQL",
    description="Привіт",
    version="1.4.8.8",
    openapi_url="/api/v2/openapi.json",  
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return {"message": "Дарова!"}


@app.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)


@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(
        text=note.text, 
        completed=note.completed
        )
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}




#USERS
@app.get("/users", response_model=List[UserList], tags=["Users"])
async def find_all_users():
    query = users.select()
    return await database.fetch_all(query)



@app.post("/users", response_model=UserList, tags=["Users"])
async def register_user(user: UserEntry):
    gID   = str(uuid.uuid1())
    gDate =str(datetime.datetime.now())
    query = users.insert().values(
        id = gID,
        username   = user.username,
        password   = pwd_context.hash(user.password),
        first_name = user.first_name,
        last_name  = user.last_name,
        gender     = user.gender,
        create_at  = gDate,
        status     = "1"
    ) 
    await database.execute(query)
    return {
        "id": gID,
        **user.dict(),
        "create_at":gDate,
        "status": "1"
    }


@app.get("/users/{userId}", response_model=UserList, tags=["Users"])
async def find_user_by_id(userId: str):
    query = users.select().where(users.c.id == userId)
    return await database.fetch_one(query)



@app.put("/users", response_model=UserList, tags=["Users"])
async def update_user(user: UserUpdate):
    gDate = str(datetime.datetime.now())
    query = users.update().\
        where(users.c.id == user.id).\
        values(
            first_name = user.first_name,
            last_name  = user.last_name,
            gender     = user.gender,
            status     = user.status,
            create_at  = gDate,
        )
    await database.execute(query)

    return await find_user_by_id(user.id)



@app.delete("/users/{userId}", tags=["Users"])
async def delete_user(user: UserDelete):
    query = users.delete().where(users.c.id == user.id)
    await database.execute(query)

    return {
        "status" : True,
        "message": "This user has been deleted successfully." 
    }





#GROUP
@app.get("/group", response_model=List[GroupList], tags=["Groups"])
async def find_all_groups():
    query = groups.select()
    return await database.fetch_all(query)



@app.post("/group", response_model=GroupList, tags=["Groups"])
async def register_group(group: GroupEntry):
    gID   = str(uuid.uuid1())
    query = groups.insert().values(
        id = gID,
        name   = group.name,
        description   = group.description,
    ) 
    await database.execute(query)
    return {
        "id": gID,
        **group.dict()
    }


@app.get("/group/{groupId}", response_model=GroupList, tags=["Groups"])
async def find_group_by_id(groupId: str):
    query = groups.select().where(groups.c.id == groupId)
    return await database.fetch_one(query)



@app.put("/groups", response_model=GroupList, tags=["Groups"])
async def update_group(group: GroupUpdate):
    gDate = str(datetime.datetime.now())
    query = groups.update().\
        where(groups.c.id == group.id).\
        values(
            name = group.name,
            description  = group.description
        )
    await database.execute(query)

    return await find_group_by_id(group.id)



@app.delete("/groups/{groupId}", tags=["Groups"])
async def delete_group(group: GroupDelete):
    query = groups.delete().where(groups.c.id == group.id)
    await database.execute(query)

    return {
        "status" : True,
        "message": "This group has been deleted successfully." 
    }