# db/database.py
import psycopg

def connect_to_postgresql(db_name: str):
    """
    Conecta ao banco de dados PostgreSQL especificado.
    :param db_name: nome do banco de dados
    :return: objeto de conexão com o banco de dados
    """
    try:
        conn = psycopg.connect(f"dbname={db_name} user=postgres password=root host=localhost port=5432")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise

# db/database.py
def create_database():
    conn = connect_to_postgresql("postgres")  # Conecta ao banco 'postgres' (banco de administração)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'monitoramento'")
    exists = cursor.fetchone()

    if not exists:
        cursor.execute("CREATE DATABASE monitoramento")
        print("Banco de dados 'monitoramento' criado com sucesso!")
    else:
        print("Banco de dados 'monitoramento' já existe.")

    cursor.close()
    conn.close()

# db/database.py
def create_tables():
    conn = connect_to_postgresql("monitoramento")  # Conecta ao banco 'monitoramento'
    cursor = conn.cursor()

    cursor.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")  # Garante que a extensão pgcrypto está instalada

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS computadores (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        mac VARCHAR(255) UNIQUE NOT NULL,
        hostname VARCHAR(255) UNIQUE NOT NULL,
        data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS discos (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        id_computador UUID NOT NULL,
        unidade VARCHAR(255) NOT NULL,
        disco_total DECIMAL(10,2) NOT NULL,
        disco_livre DECIMAL(10,2) NOT NULL,
        disk_percent DECIMAL(5,2) NOT NULL,
        data_coleta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_computador FOREIGN KEY (id_computador) REFERENCES computadores(id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dados_monitoramento (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        id_computador UUID REFERENCES computadores(id) ON DELETE CASCADE,
        id_discos UUID REFERENCES discos(id) ON DELETE CASCADE,
        hostname VARCHAR(255),
        cpu_info VARCHAR(255),
        cpu_percent DECIMAL(5,2),
        memoria_total DECIMAL(10,2),
        memoria_livre DECIMAL(10,2),
        ram_percent DECIMAL(5,2),
        ip_local VARCHAR(255),
        data_coleta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()  # Comita as alterações no banco de dados
    print("Tabelas criadas com sucesso!")

    cursor.close()
    conn.close()
