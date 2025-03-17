from fastapi import APIRouter
from domain.entities.Cliente import Cliente

# import da persistência
import db
from infra.orm.ClienteModel import ClienteDB

#import de segurança
from typing import Annotated
from fastapi import Depends
from security import get_current_active_user, User

# Eduardo Tortelli

router = APIRouter(dependencies=[Depends(get_current_active_user)])

# Criar os endpoints de Cliente: GET, POST, PUT, DELETE

@router.get("/cliente/", tags=["Cliente"])
async def get_cliente():
    try:
        session = db.Session()

        # busca todos
        dados = session.query(ClienteDB).all()

        return dados, 200

    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/cliente/{id}", tags=["Cliente"])
async def get_cliente(id: int):
    try:
        session = db.Session()
        
        # busca um com filtro
        dados = session.query(ClienteDB).filter(ClienteDB.id_cliente == id).all()

        return dados, 200

    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/cliente/", tags=["Cliente"])
async def post_cliente(corpo: Cliente):
    try:
        session = db.Session()

        # cria um novo objeto com os dados da requisição
        dados = ClienteDB(None, corpo.nome, corpo.cpf, corpo.telefone)


        session.add(dados)
        # session.flush()
        session.commit()

        return {"id": dados.id_cliente}, 200

    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/cliente/{id}", tags=["Cliente"])
async def put_cliente(id: int, corpo: Cliente):
    try:
        session = db.Session()
        
        # busca os dados atuais pelo id
        dados = session.query(ClienteDB).filter(ClienteDB.id_cliente == id).one()

        # atualiza os dados com base no corpo da requisição
        dados.nome = corpo.nome
        dados.cpf = corpo.cpf
        dados.telefone = corpo.telefone
        
        session.add(dados)
        session.commit()

        return {"id": dados.id_cliente}, 200
    
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/cliente/{id}", tags=["Cliente"])
async def delete_cliente(id: int):
    try:
        session = db.Session()
        # busca os dados atuais pelo id
        dados = session.query(ClienteDB).filter(ClienteDB.id_cliente == id).one()
        session.delete(dados)
        session.commit()

        return {"id": dados.id_cliente}, 200

    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# valida o cpf e senha informado pelo usuário
@router.post("/cliente/login/", tags=["Cliente - Login"])
async def login_cliente(corpo: Cliente):
    try:
        session = db.Session()

        # one(), requer que haja apenas um resultado no conjunto de resultados
        # é um erro se o banco de dados retornar 0, 2 ou mais resultados e uma exceção será gerada
        dados = session.query(ClienteDB).filter(ClienteDB.cpf == corpo.cpf).filter(ClienteDB.nome == corpo.nome).one()
        
        return dados, 200

    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

# verifica se o CPF informado já esta cadastrado, retornado os dados atuais caso já esteja
@router.get("/cliente/cpf/{cpf}", tags=["Cliente - Valida CPF"])
async def cpf_cliente(cpf: str):
    try:
        session = db.Session()

        # busca um com filtro, retornando os dados cadastrados
        dados = session.query(ClienteDB).filter(ClienteDB.cpf == cpf).all()

        return dados, 200

    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()