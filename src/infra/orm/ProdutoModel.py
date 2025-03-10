import db
from sqlalchemy import Column, VARCHAR, CHAR, Integer

# ORM

class ProdutoDB(db.Base):
    __tablename__ = 'tb_produto'

    id_produto = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(VARCHAR(100), nullable=False)
    descricao = Column(VARCHAR(250), nullable=False)
    # foto = Column(LargeBinary, nullable=True)  # Representa BLOB para imagens
    valor_unitario = Column(VARCHAR(20), nullable=False)


    def __init__(self, id_produto, nome, descricao, valor_unitario):
        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.valor_unitario = valor_unitario