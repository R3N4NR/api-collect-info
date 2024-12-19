from fastapi import APIRouter, HTTPException
from app.database.database import connect_to_postgresql
from app.schemas.DadosDiscos import CreateDiscos

router = APIRouter()

@router.post("/create-disks", summary="Encriptar e gravar dados de discos", response_model=CreateDiscos)
def create_disks(discos: CreateDiscos):
    try:
        # Converte o UUID para string e prepara os dados para inserção
        dados_dict = {key: str(value) for key, value in discos.dict().items()}
        id_computador = dados_dict.pop('id_computador', None)
        if not id_computador:
            raise HTTPException(status_code=400, detail="Campo 'id_computador' ausente.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar os dados: {str(e)}")

    try:
        # Conectar ao banco de dados
        with connect_to_postgresql("monitoramento") as conn:
            cursor = conn.cursor()

            # Verifica se o computador já existe
            cursor.execute(
                '''SELECT id FROM discos WHERE id_computador = %s''',
                (id_computador,)
            )
            existing_computer = cursor.fetchone()

            if existing_computer:
                raise HTTPException(
                    status_code=409,
                    detail=f"O computador {id_computador} já existe na tabela discos."
                )

            # Insere os dados no banco de dados
            cursor.execute(
                '''INSERT INTO discos (
                    id_computador, unidade, disco_total, disco_livre, disk_percent
                ) VALUES (%s, %s, %s, %s, %s)
                RETURNING id''',
                (
                    discos.id_computador,
                    discos.unidade,
                    discos.disco_total, 
                    discos.disco_livre,
                    discos.disk_percent
                )
            )

            # Confirmar a transação
            conn.commit()

            return {
                "id_computador":discos.id_computador,
                "unidade":discos.unidade,
                "disco_total":discos.disco_total,
                "disco_livre":discos.disco_livre,
                "disk_percent":discos.disk_percent
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar o banco de dados: {str(e)}")
