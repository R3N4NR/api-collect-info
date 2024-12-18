# app/main.py
from fastapi import FastAPI
from app.database.database import connect_to_postgresql, create_database, create_tables
from app.routers import router_create_computer, router_create_metrics,router_create_disco, router_list_computer

app = FastAPI()

# Incluindo as rotas no aplicativo FastAPI
app.include_router(router_create_computer)  # Rota create-computer
app.include_router(router_create_metrics)  # Rota create-metrics
app.include_router(router_create_disco)
app.include_router(router_list_computer)


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
