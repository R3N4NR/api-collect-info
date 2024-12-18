from fastapi import APIRouter, HTTPException
from app.schemas.DadosDiscos import CreateDiscos
from app.security.encryptDecrypt import desencriptar_dados, encriptar_dados

router = APIRouter()

@router.post("/create-disks", summary="Encriptar ou desencriptar dados de monitoramento", response_model=CreateDiscos)
def dados_disco(dados: CreateDiscos, acao: str = "encriptar"):
    try:
        dados_dict = dados.dict()

        if acao == "encriptar":
            dados_encriptados = encriptar_dados(dados_dict)  # Encriptar os dados
            return {"dados_encriptados": dados_encriptados}
        elif acao == "desencriptar":
            dados_descriptografados = desencriptar_dados(dados_dict)  # Desencriptar os dados
            return {"dados_descriptografados": dados_descriptografados}
        else:
            raise HTTPException(status_code=400, detail="Ação inválida. Use 'encriptar' ou 'desencriptar'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar os dados: {str(e)}")