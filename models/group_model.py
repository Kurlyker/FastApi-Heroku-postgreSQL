from pydantic import BaseModel, Field

## Models
class GroupList(BaseModel):
    id           : str
    name         : str
    description  : str
class GroupEntry(BaseModel):
    name         : str = Field(..., example="NameGroup")
    description  : str = Field(..., example="description bla bla bla")
class GroupUpdate(BaseModel):
    id           : str = Field(..., example="Enter your id")
    name         : str = Field(..., example="NameGroup")
    description  : str = Field(..., example="Updated description bla bla bla Updated")

class GroupDelete(BaseModel):
    id: str = Field(..., example="Enter your id")