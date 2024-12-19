# app/main.py
from fastapi import FastAPI
from app.database.database import create_database, create_tables
from app.routers.routers import routers  # Importa todas as rotas como um grupo

app = FastAPI()

# Incluindo todas as rotas em um loop
for router in routers:
    app.include_router(router)

@app.get("/create-database")
def create_db():
    create_database()
    return {"message": "Banco de dados criado com sucesso!"}

@app.get("/create-tables")
def create_db_tables():
    create_tables()
    return {"message": "Tabelas criadas com sucesso!"}
    
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API!"}