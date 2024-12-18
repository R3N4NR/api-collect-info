import uuid
from fastapi import APIRouter, HTTPException
from app.schemas.DadosMonitoramento import CreateMonitoramento
from app.security.encryptDecrypt import encriptar_dados
from app.database.database import connect_to_postgresql
import logging


router = APIRouter()

from app.security.encryptDecrypt import desencriptar_dados

@router.post("/create-metrics", summary="Encriptar e gravar dados de monitoramento", response_model=CreateMonitoramento)
def create_monitoramento(monitoramento: CreateMonitoramento):
    try:
        dados_dict = monitoramento.dict()
    # Converte o UUID para string antes de encriptar
        dados_dict = {key: str(value) for key, value in dados_dict.items()}
    
    # Extrai o id_computador e o IP para tratamento separado
        id_computador = str(dados_dict.pop('id_computador'))
        ip_local = dados_dict['ip_local']  # Armazena o IP original

    # Criptografa apenas o IP
        ip_encriptado = encriptar_dados({"ip_local": ip_local})['ip_local']
        dados_dict['ip_local'] = ip_encriptado  # Substitui o IP pelo valor criptografado

    # Conectar ao banco de dados
        conn = connect_to_postgresql("monitoramento")
        cursor = conn.cursor()

    # Verifica se o computador já existe
        cursor.execute(
            '''SELECT id FROM dados_monitoramento WHERE id_computador = %s''', 
            (id_computador,)  # Envolvido em uma tupla
        )
        existing_computer = cursor.fetchone()
        print(existing_computer)

        if not existing_computer:
            # Se o computador não existe, insere um novo registro
            cursor.execute(
            '''INSERT INTO dados_monitoramento (hostname, id_computador, ip_local, cpu_info, cpu_percent,
                                                memoria_total, memoria_livre, ram_percent)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id''',
            (
                dados_dict['hostname'],  # Dados em texto
                id_computador,          # UUID como string
                dados_dict['ip_local'], # IP criptografado
                dados_dict['cpu_info'],
                dados_dict['cpu_percent'],
                dados_dict['memoria_total'],
                dados_dict['memoria_livre'],
                dados_dict['ram_percent']
            )
        )

        # Confirmar a transação e fechar a conexão
        conn.commit()
        cursor.close()
        conn.close()

        return {
            "hostname": monitoramento.hostname,
            "id_computador": monitoramento.id_computador,
            "ip_local": monitoramento.ip_local,
            "cpu_info": monitoramento.cpu_info,
            "cpu_percent": monitoramento.cpu_percent,
            "memoria_total": monitoramento.memoria_total,
            "memoria_livre": monitoramento.memoria_livre,
            "ram_percent": monitoramento.ram_percent,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar os dados: {str(e)}")

