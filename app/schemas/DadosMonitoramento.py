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
    