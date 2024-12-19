import uuid
from fastapi import APIRouter, HTTPException
from app.schemas.DadosMonitoramento import UpdateMonitoramento
from app.security.encryptDecrypt import encriptar_dados, desencriptar_dados
from app.database.database import connect_to_postgresql
from datetime import datetime

router = APIRouter()

@router.put("/update-metrics", summary="Atualizar dados de monitoramento", response_model=UpdateMonitoramento)
def update_monitoramento(id: uuid.UUID, monitoramento: UpdateMonitoramento):
    try:
        # Converte o UUID para string e prepara os dados para atualização
        dados_dict = {key: str(value) for key, value in monitoramento.dict().items()}

        ip_local = dados_dict.get('ip_local', None)
        if not ip_local:
            raise HTTPException(status_code=400, detail="Campo 'ip_local' ausente.")

        # Criptografa o IP
        ip_encriptado = encriptar_dados({"ip_local": ip_local})['ip_local']
        dados_dict['ip_local'] = ip_encriptado

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar os dados: {str(e)}")

    try:
        # Conectar ao banco de dados
        with connect_to_postgresql("monitoramento") as conn:
            cursor = conn.cursor()

            # Verifica se o registro existe no banco
            cursor.execute(
                '''SELECT id FROM dados_monitoramento WHERE id = %s''',
                (str(id),)
            )
            existing_computer = cursor.fetchone()

            if not existing_computer:
                raise HTTPException(
                    status_code=404,
                    detail=f"O registro com ID {id} não foi encontrado na tabela monitoramento."
                )

            # Atualiza os dados no banco de dados
            cursor.execute(
                '''UPDATE dados_monitoramento
                   SET hostname = %s, ip_local = %s, cpu_info = %s, cpu_percent = %s,
                       memoria_total = %s, memoria_livre = %s, ram_percent = %s, data_coleta = %s
                   WHERE id = %s''',
                (
                    dados_dict['hostname'],            
                    dados_dict['ip_local'],  
                    dados_dict['cpu_info'],
                    dados_dict['cpu_percent'],
                    dados_dict['memoria_total'],
                    dados_dict['memoria_livre'],
                    dados_dict['ram_percent'],
                    datetime.now(),          
                    str(id)                  
                )
            )

            # Confirmar a transação
            conn.commit()

            return {
                "id": id,
                "hostname": dados_dict['hostname'] ,
                "ip_local": dados_dict['ip_local'] ,
                "cpu_info": dados_dict['cpu_info'],
                "cpu_percent": dados_dict['cpu_percent'],
                "memoria_total": dados_dict['memoria_total'],
                "memoria_livre": dados_dict['memoria_livre'],
                "ram_percent": dados_dict['ram_percent'],
                "data_coleta": datetime.now()
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar o banco de dados: {str(e)}")
