from datetime import datetime
import uuid
from pydantic import BaseModel

class CreateDiscos(BaseModel):
    id_computador:uuid.UUID
    unidade:str
    disco_total:float
    disco_livre:float
    disk_percent:float
    
class ListDisks(BaseModel):
    id: uuid.UUID
    id_computador: uuid.UUID
    unidade: str
    disco_total: float
    disco_livre: float
    disk_percent: float
    data_coleta: datetime
    
class UpdateDiscos(BaseModel):
    unidade:str
    disco_total:float
    disco_livre:float
    disk_percent:float
    
    