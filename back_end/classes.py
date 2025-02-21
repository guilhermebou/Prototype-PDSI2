from pydantic import BaseModel
from datetime import datetime

class Mensagem(BaseModel):
    titulo: str
    conteudo: str
    publicada: bool = True

class Menu(BaseModel):
    id: int
    titulo: str
    url: str
    created_at: datetime

    class Config:
        from_attributes = True
