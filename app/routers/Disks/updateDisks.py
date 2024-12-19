import uuid
from fastapi import APIRouter, HTTPException
from app.database.database import connect_to_postgresql
from app.schemas.DadosDiscos import UpdateDiscos
from datetime import datetime

router = APIRouter()

@router.put("/update-disks", summary="Atualizar dados de discos", response_model=UpdateDiscos)
def update_disks(id: uuid.UUID, discos: UpdateDiscos):
    try:
        # Converte o UUID para string e prepara os dados para atualização
        dados_dict = {key: str(value) for key, value in discos.dict().items()}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar os dados: {str(e)}")

    try:
        # Conectar ao banco de dados
        with connect_to_postgresql("monitoramento") as conn:
            cursor = conn.cursor()

            # Verifica se o disco já existe para o computador fornecido
            cursor.execute(
                '''SELECT id FROM discos WHERE id = %s''',
                (str(id),)
            )
            existing_disk = cursor.fetchone()

            if existing_disk:
                # Se o disco existe, faz o update
                cursor.execute(
                    '''UPDATE discos 
                    SET unidade = %s, disco_total = %s, disco_livre = %s, disk_percent = %s, data_coleta = %s 
                    WHERE id = %s''',
                    (
                        dados_dict['unidade'],
                        dados_dict['disco_total'], 
                        dados_dict['disco_livre'],
                        dados_dict['disk_percent'],
                        datetime.now(),
                        str(id),
                        
                    )
                )
           
            # Confirmar a transação
            conn.commit()

            return {
                "id": id,
                "unidade": discos.unidade,
                "disco_total": discos.disco_total,
                "disco_livre": discos.disco_livre,
                "disk_percent": discos.disk_percent,
                "data_coleta": datetime.now()
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar o banco de dados: {str(e)}")
