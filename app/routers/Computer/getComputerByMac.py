from fastapi import APIRouter, HTTPException
from app.schemas.DadosComputador import ListComputador
from app.security.encryptDecrypt import desencriptar_dados, encriptar_dados
from app.database.database import connect_to_postgresql
import logging

router = APIRouter()

@router.get("/get-computador-by-mac", summary="Buscar computador por MAC", response_model=ListComputador)
def get_computador_by_mac(mac: str):
    try:
        # Encriptar o MAC passado para compará-lo com o MAC encriptado no banco
        mac_encriptado = encriptar_dados({"mac": mac})["mac"]
        
        # Conectar ao banco de dados
        conn = connect_to_postgresql('monitoramento')
        cursor = conn.cursor()

        # Buscar o id_computador com base no mac encriptado
        cursor.execute(
            '''SELECT c.id, c.hostname, c.mac, c.data_registro 
               FROM computadores c
               JOIN dados_monitoramento d ON d.id_computador = c.id
               WHERE c.mac = %s''',  # Comparando com o MAC encriptado
            (mac_encriptado,)  # Passando o MAC encriptado como parâmetro
        )
        computador = cursor.fetchone()

        if not computador:
            raise HTTPException(status_code=404, detail="Computador não encontrado para o MAC fornecido")

        # Desempacotar os dados do computador
        id, hostname, mac, data_registro = computador

        # Desencriptar o mac retornado para exibir de forma legível
        mac_desencriptado = desencriptar_dados({"mac": mac})["mac"]

        # Colocar os dados em um dicionário
        dados_dict = {
            "id": id,
            "hostname": str(hostname),
            "mac": mac_desencriptado,  # Passando o MAC desencriptado
            "data_registro": str(data_registro)
        }

        # Fechar a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Retornar os dados desencriptados
        return ListComputador(**dados_dict)

    except Exception as e:
        logging.error(f"Erro ao processar os dados: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar os dados: {str(e)}")
