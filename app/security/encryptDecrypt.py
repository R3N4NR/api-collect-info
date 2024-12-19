import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()  # Isso carrega as variáveis de ambiente para o ambiente Python

# A chave será lida da variável de ambiente
chave = os.getenv("CHAVE_CRIPTOGRAFIA")  # Lê a chave do .env
if chave is None:
    raise ValueError("A chave de criptografia não foi definida na variável de ambiente.")

fernet = Fernet(chave)

# Função de encriptação
def encriptar_dados(dados_dict):
    dados_encriptados = {}
    for chave, valor in dados_dict.items():
        # Encripta o valor e converte para base64
        valor_encriptado = fernet.encrypt(valor.encode()).decode('utf-8')
        dados_encriptados[chave] = valor_encriptado
    return dados_encriptados

# Função de desencriptação
def desencriptar_dados(dados_dict):
    desencriptados = {}
    for chave, valor_encriptado in dados_dict.items():
        try:
            # Desencripta a string encriptada diretamente com fernet
            valor_desencriptado = fernet.decrypt(valor_encriptado.encode()).decode('utf-8')  # Desencripta a string
            desencriptados[chave] = valor_desencriptado
        except Exception as e:
            # Se não conseguir desencriptar, mantemos o valor original (caso não tenha sido encriptado)
            desencriptados[chave] = valor_encriptado
    return desencriptados
