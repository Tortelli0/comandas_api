from fastapi import APIRouter
from domain.entities.Produto import Produto
import db
from infra.orm.ProdutoModel import ProdutoDB
# import da persistência

#import de segurança
from typing import Annotated
from fastapi import Depends
from security import get_current_active_user, User

# Eduardo Tortelli

router = APIRouter(dependencies=[Depends(get_current_active_user)])

# Criar as rotas/endpoints: GET, POST, PUT, DELETE

@router.get("/produto/", tags=["Produto"])
async def get_produto():
    try:
        session = db.Session()

        # busca todos
        dados = session.query(ProdutoDB).all()

        return dados, 200

    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/produto/{id}", tags=["Produto"])
async def get_produto(id: int):
    try:
        session = db.Session()

        # busca um com filtro
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).all()

        return dados, 200

    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/produto/", tags=["Produto"])
async def post_produto(corpo: Produto):
    try:
        session = db.Session()

        # cria um novo objeto com os dados da requisição
        dados = ProdutoDB(None, corpo.nome, corpo.descricao, corpo.valor_unitario)

        session.add(dados)
        # session.flush()
        session.commit()

        return {"id": dados.id_produto}, 200
  
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/produto/{id}", tags=["Produto"])
async def put_produto(id: int, corpo: Produto):
    try:
        session = db.Session()
        
        # Busca os dados atuais pelo id
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one()
        
        # Atualiza os dados com base no corpo da requisição
        dados.nome = corpo.nome
        dados.descricao = corpo.descricao
        # dados.foto = corpo.foto
        dados.valor_unitario = corpo.valor_unitario
        
        session.add(dados)
        session.commit()
        
        return {"id": dados.id_produto}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/produto/{id}", tags=["Produto"])
async def delete_produto(id: int):
    try:
        session = db.Session()
        # Busca os dados atuais pelo id
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one()
        session.delete(dados)
        session.commit()
        
        return {"id": dados.id_produto}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Valida um produto por algum critério (exemplo: nome e um código de segurança)
@router.post("/produto/login/", tags=["Produto - Login"])
async def login_produto(corpo: Produto):
    try:
        session = db.Session()
        
        # Busca um produto pelo nome e (exemplo) uma chave de segurança
        dados = session.query(ProdutoDB).filter(ProdutoDB.nome == corpo.nome).filter(ProdutoDB.valor_unitario == corpo.valor_unitario).one()
        
        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Verifica se o nome do produto já está cadastrado, retornando os dados atuais caso esteja
@router.get("/produto/nome/{nome}", tags=["Produto - Valida Nome"])
async def nome_produto(nome: str):
    try:
        session = db.Session()
        
        # Busca um produto pelo nome
        dados = session.query(ProdutoDB).filter(ProdutoDB.nome == nome).all()
        
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()
