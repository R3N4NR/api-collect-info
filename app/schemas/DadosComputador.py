
from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel

class CreateComputador(BaseModel):
    hostname:str
    mac:str
    
class ListComputador(BaseModel):
    id: uuid.UUID
    hostname: str
    mac: str
    data_registro: datetime
