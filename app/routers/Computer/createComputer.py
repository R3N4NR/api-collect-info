from fastapi import APIRouter, HTTPException
from app.schemas.DadosComputador import CreateComputador
from app.security.encryptDecrypt import encriptar_dados
from app.database.database import connect_to_postgresql


router = APIRouter()

@router.post("/create-computer", summary="Encriptar e gravar dados do computador", response_model=CreateComputador)
def create_computador(computador: CreateComputador):
    try:
        dados_dict = computador.dict()
        print(dados_dict)
        
        # Encriptar os dados e armazená-los no banco
        dados_encriptados = encriptar_dados(dados_dict)
        print(dados_encriptados)
        
        # Conectar ao banco e gravar os dados encriptados
        conn = connect_to_postgresql("monitoramento")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO computadores (mac, hostname)
            VALUES (%s, %s)
            RETURNING id;
        ''', (dados_encriptados["mac"], dados_encriptados["hostname"]))  # Enviar os dados encriptados para o banco
        
        conn.commit()
        cursor.close()
        conn.close()

        return {
            "hostname": computador.hostname,  # Incluindo hostname na resposta
            "mac": computador.mac  # Incluindo mac na resposta
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar os dados: {str(e)}")
