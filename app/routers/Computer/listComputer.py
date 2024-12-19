import uuid
from fastapi import APIRouter, HTTPException
from app.schemas.DadosComputador import ListComputador
from app.security.encryptDecrypt import desencriptar_dados
from app.database.database import connect_to_postgresql

router = APIRouter()

@router.get("/list-computer", summary="Desencriptar e ler dados de computador", response_model=ListComputador)
def list_computador(id: uuid.UUID):
    try:
        # Conectar ao banco de dados
        conn = connect_to_postgresql('monitoramento')
        cursor = conn.cursor()

        # Buscar os dados do computador no banco de dados
        cursor.execute(
            "SELECT id, hostname, mac, data_registro FROM computadores WHERE id = %s",
            (str(id),)  # Passando o `id` como string
        )
        computador = cursor.fetchone()

        if not computador:
            raise HTTPException(status_code=404, detail="Computador não encontrado")

        # Desempacotar os dados do computador
        id, hostname, mac, data_registro = computador

        # Colocar os dados em um dicionário
        dados_dict = {
            "id": id,
            "hostname": str(hostname),
            "mac": str(mac),
            "data_registro": str(data_registro)
        }

        # Desencriptar os dados
        dados_desencriptados = desencriptar_dados(dados_dict)

        # Fechar a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Retornar os dados desencriptados
        return ListComputador(**dados_desencriptados)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar os dados: {str(e)}")

