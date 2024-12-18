from pydantic import BaseModel

class CreateDiscos(BaseModel):
    id_computador:str 
    disco:str
    disco_total:str
    disco_livre:str
    disk_percent:str