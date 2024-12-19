from typing import List
from fastapi import APIRouter, HTTPException
from app.security.encryptDecrypt import desencriptar_dados
from app.database.database import connect_to_postgresql
from app.schemas.DadosComputador import ListComputador
import logging

router = APIRouter()

@router.get("/list-computer", summary="Buscar todos os computadores e comparar o MAC", response_model=List[ListComputador])
def list_computadores(mac: str):
    try:
        # Conectar ao banco de dados
        conn = connect_to_postgresql('monitoramento')
        cursor = conn.cursor()

        # Buscar todos os computadores
        cursor.execute(
            "SELECT id, hostname, mac, data_registro FROM computadores"
        )
        computadores = cursor.fetchall()

        if not computadores:
            raise HTTPException(status_code=404, detail="Nenhum computador encontrado")

        # Lista para armazenar os computadores encontrados com o MAC correspondente
        computadores_desencriptados = []

        # Desencriptar e comparar o MAC de cada computador
        for computador in computadores:
            id, hostname, mac_banco, data_registro = computador

            # Desencriptar o MAC
            mac_desencriptado = desencriptar_dados({"mac": mac_banco})["mac"]
            
            if mac_desencriptado == mac:
                # Colocar os dados desencriptados em um dicionário
                dados_dict = {
                    "id": id,
                    "hostname": str(hostname),
                    "mac": mac_desencriptado,  # Passando o MAC desencriptado
                    "data_registro": str(data_registro),
                }

                # Adicionar o computador à lista de resultados
                computadores_desencriptados.append(ListComputador(**dados_dict))

        cursor.close()
        conn.close()

        if not computadores_desencriptados:
            raise HTTPException(status_code=404, detail="Nenhum computador com MAC correspondente encontrado")

        # Retornar os computadores desencriptados que correspondem ao MAC
        return computadores_desencriptados

    except Exception as e:
        logging.error(f"Erro ao processar os dados: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar os dados: {str(e)}")
