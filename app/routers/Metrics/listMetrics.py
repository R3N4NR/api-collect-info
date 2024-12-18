import uuid
from fastapi import APIRouter, HTTPException
from app.schemas.DadosComputador import ListComputador
from app.schemas.DadosMonitoramento import ListMonitoramento
from app.security.encryptDecrypt import desencriptar_dados
from app.database.database import connect_to_postgresql

router = APIRouter()

@router.get("/list-monitoramento", summary="Desencriptar e ler dados de monitoramento", response_model=ListMonitoramento)
def list_monitoramento(id: uuid.UUID):
    try:
        # Conectar ao banco de dados
        conn = connect_to_postgresql('monitoramento')
        cursor = conn.cursor()

        # Buscar os dados do computador no banco de dados
        cursor.execute(
            '''SELECT id, hostname, id_discos, id_computador, ip_local, cpu_info,
            cpu_percent, memoria_total, memoria_livre, ram_percent, data_coleta
            FROM dados_monitoramento WHERE id = %s''',
            (str(id),)  # Certifique-se de que id está sendo passado corretamente
        )
        monitoramento = cursor.fetchone()

        if not monitoramento:
            raise HTTPException(status_code=404, detail="Não há dados de monitoramento para esse computador")

        # Desempacotar os dados do computador
        valores_convertidos = tuple(str(valor) for valor in monitoramento)

        # Desempacota os valores convertidos
        id, hostname, id_discos, id_computador, ip_local, cpu_info, cpu_percent, memoria_total, memoria_livre, ram_percent, data_coleta = valores_convertidos

        # Colocar os dados em um dicionário
        dados_dict = {
            "id": id,
            "hostname": hostname,
            "id_discos": id_discos,
            "id_computador": id_computador,
            "data_coleta": data_coleta,
            "cpu_info": cpu_info,
            "cpu_percent": cpu_percent,
            "memoria_total": memoria_total,
            "memoria_livre": memoria_livre,
            "ram_percent": ram_percent
        }

        # Desencriptar os dados
        ip_desencriptado = desencriptar_dados({"ip_local": ip_local})['ip_local']

        # Fechar a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Retornar os dados desencriptados usando ListMonitoramento (não ListComputador)
        return ListMonitoramento(
            id=uuid.UUID(id),  # Garantir que o ID seja do tipo UUID
            hostname=dados_dict['hostname'],
            id_discos=dados_dict['id_discos'],
            id_computador=dados_dict['id_computador'],
            data_coleta=dados_dict['data_coleta'],
            ip_local=ip_desencriptado,  # Passando diretamente o valor desencriptado
            cpu_info=dados_dict['cpu_info'],
            cpu_percent=dados_dict['cpu_percent'],
            memoria_total=dados_dict['memoria_total'],
            memoria_livre=dados_dict['memoria_livre'],
            ram_percent=dados_dict['ram_percent']
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar os dados: {str(e)}")
