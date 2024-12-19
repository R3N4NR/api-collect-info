PARA EXECUTAR A API

uvicorn app.main:app --reload


Essa é uma API desenvolvida com FastAPI. O objetivo dessa API é fazer a manipulação de um banco de dados POSTGRESQL onde estarão armazenados dados de métrica do computador.

libs utilizadas

psycopg (DEVE SER A VERSÃO 3)
dotenv 
logging
pydantic
Fernet
