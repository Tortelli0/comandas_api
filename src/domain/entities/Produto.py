from pydantic import BaseModel
# Eduardo Tortelli

class Produto(BaseModel):
    id_produto: int = None
    nome: str
    descricao: str
    # foto: bytes | None = None  # Representando BLOB
    valor_unitario: str