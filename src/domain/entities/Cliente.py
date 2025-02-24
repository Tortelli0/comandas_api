from pydantic import BaseModel
# Eduardo Tortelli

class Cliente(BaseModel):
    id_cliente: int = None
    nome: str
    cpf: str
    telefone: str = None