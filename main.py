from typing import List

import databases

import sqlalchemy

from fastapi import FastAPI
from pydantic import BaseModel


DATABASE_URL = "postgresql://kxcmhbkhvyyfel:bcea7a52633f6d2b8278c4880343774c2166835491d099bc28e3300e7d1ca5ba@ec2-52-213-119-221.eu-west-1.compute.amazonaws.com:5432/d7c6o4a367jfbo"

database = databases.Database(DATABASE_URL)


metadata = sqlalchemy.MetaData()



notes = sqlalchemy.Table(

    "notes",

    metadata,

    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),

    sqlalchemy.Column("text", sqlalchemy.String),

    sqlalchemy.Column("completed", sqlalchemy.Boolean),

)



engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool


app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="професиANAL PROGRAMMING",
    description="Кто прочитал тот сдохнет",
    version="2.0",
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


