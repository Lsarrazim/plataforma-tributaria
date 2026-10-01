import sqlite3
from pathlib import Path

#Caminho do banco de dados 
DB_PATH = Path(__file__).resolve().parent.parent.parent /"dados.db"

def obter_conexao(caminho: Path = DB_PATH) -> sqlite3.Connection:
    """
    Abre uma conexão com o banco
    row_factory = sqlite3.Row permite acessar colunas por nome
    (linha["valor"]) em vez de por indice (linha[2]) - mais legível
    """
    conexao = sqlite3.connect(caminho)
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_tabelas(caminho: Path = DB_PATH) -> None:
    conexao = obter_conexao(caminho)
    conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS calculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mensagem TEXT NOT NULL,
            valor REAL NOT NULL,
            aliquota REAL NOT NULL,
            resultado REAL NOT NULL,
            criado_em TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
    )
    conexao.commit()
    conexao.close()
