import uuid
from fastapi import APIRouter, HTTPException
from app.schemas.DadosDiscos import ListDisks
from app.database.database import connect_to_postgresql
import logging

router = APIRouter()

@router.get("/list-disks", summary="Desencriptar e ler dados de discos", response_model=ListDisks)
def list_disks(id_computador: uuid.UUID):
    try:
        # Conectar ao banco de dados
        conn = connect_to_postgresql('monitoramento')
        cursor = conn.cursor()

        # Converter UUID para string
        id_computador_str = str(id_computador)

        logging.info(f"Buscando dados para o ID do computador: {id_computador_str}")

        # Buscar os dados do computador no banco de dados
        cursor.execute(
            "SELECT id, id_computador, unidade, disco_total, disco_livre, disk_percent, data_coleta FROM discos WHERE id_computador = %s",
            (id_computador_str,)  # Passa o UUID convertido para string
        )
        discos = cursor.fetchone()

        # Verificar se a consulta retornou resultados
        if not discos:
            raise HTTPException(status_code=404, detail="Disco não encontrado no banco de dados")

        # Desempacotar os dados do disco
        id, id_computador, unidade, disco_total, disco_livre, disk_percent, data_coleta = discos

        # Fechar a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Retornar os dados desencriptados
        return ListDisks(
            id=id,
            id_computador=id_computador,
            unidade=unidade,
            disco_total=disco_total,
            disco_livre=disco_livre,
            disk_percent=disk_percent,
            data_coleta=data_coleta
        )

    except Exception as e:
        logging.error(f"Erro ao processar os dados: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar os dados: {str(e)}")
