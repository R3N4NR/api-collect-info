from datetime import datetime
import uuid
from pydantic import BaseModel


class CreateMonitoramento(BaseModel):
    hostname: str
    id_computador:uuid.UUID
    ip_local: str
    cpu_info: str
    cpu_percent: float
    memoria_total: float
    memoria_livre: float
    ram_percent: float
    
class ListMonitoramento(BaseModel):
    id:uuid.UUID
    id_discos : str
    hostname: str
    id_computador:uuid.UUID
    ip_local: str
    cpu_info: str
    cpu_percent: float
    memoria_total: float
    memoria_livre: float
    ram_percent: float
    data_coleta: datetime

class UpdateMonitoramento(BaseModel):
    hostname: str
    ip_local: str
    cpu_info: str
    cpu_percent: float
    memoria_total: float
    memoria_livre: float
    ram_percent: float
    
    
    