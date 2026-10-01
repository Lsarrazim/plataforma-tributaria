from pathlib import Path
from app.db.database import obter_conexao, DB_PATH

def salvar_calculo(
        mensagem: str, valor: float, aliquota: float, resultado: float, caminho: Path = DB_PATH
) -> None:
    conexao = obter_conexao(caminho)
    conexao.execute(
        """
        INSERT INTO calculos (mensagem, valor, aliquota, resultado)
        VALUES (?, ?, ?, ?)
        """,
        (mensagem, valor, aliquota, resultado),
    )
    conexao.commit()
    conexao.close()

def listar_calculos(caminho: Path = DB_PATH) -> list[dict]:
    conexao = obter_conexao(caminho)
    linhas = conexao.execute(
        "SELECT * FROM calculos ORDER BY criado_em DESC"
    ).fetchall()
    conexao.close()
    return [dict(linha) for linha in linhas]