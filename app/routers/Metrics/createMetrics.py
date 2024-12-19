import uuid
from fastapi import APIRouter, HTTPException
from app.schemas.DadosMonitoramento import CreateMonitoramento
from app.security.encryptDecrypt import encriptar_dados, desencriptar_dados
from app.database.database import connect_to_postgresql

router = APIRouter()

@router.post("/create-metrics", summary="Encriptar e gravar dados de monitoramento", response_model=CreateMonitoramento)
def create_monitoramento(monitoramento: CreateMonitoramento):
    try:
        # Converte o UUID para string e prepara os dados para inserção
        dados_dict = {key: str(value) for key, value in monitoramento.dict().items()}
        id_computador = dados_dict.pop('id_computador', None)
        if not id_computador:
            raise HTTPException(status_code=400, detail="Campo 'id_computador' ausente.")

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

            # Verifica se o computador já existe
            cursor.execute(
                '''SELECT id FROM dados_monitoramento WHERE id_computador = %s''',
                (id_computador,)
            )
            existing_computer = cursor.fetchone()

            if existing_computer:
                raise HTTPException(
                    status_code=409,
                    detail=f"O computador {id_computador} já existe na tabela monitoramento."
                )

            # Insere os dados no banco de dados
            cursor.execute(
                '''INSERT INTO dados_monitoramento (
                    hostname, id_computador, ip_local, cpu_info, cpu_percent,
                    memoria_total, memoria_livre, ram_percent
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id''',
                (
                    dados_dict['hostname'],  # Dados em texto
                    id_computador,           # UUID como string
                    dados_dict['ip_local'],  # IP criptografado
                    dados_dict['cpu_info'],
                    dados_dict['cpu_percent'],
                    dados_dict['memoria_total'],
                    dados_dict['memoria_livre'],
                    dados_dict['ram_percent']
                )
            )

            # Confirmar a transação
            conn.commit()

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
        raise HTTPException(status_code=500, detail=f"Erro ao acessar o banco de dados: {str(e)}")
