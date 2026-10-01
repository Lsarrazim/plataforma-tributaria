from app.db.database import criar_tabelas
from app.repositories.calculo_repository import salvar_calculo, listar_calculos

def test_salvar_e_listar_calculo(tmp_path):
    """
    tmp_path é fixture nativa do pytest: cria uma pasta temporaria
    unica para cada teste, apagando automaticamente depois, isso garante
    que o teste nunca escreve no dados.db real do projeto
    """

    banco_temporario = tmp_path / "teste.db"
    criar_tabelas(banco_temporario)

    salvar_calculo(
        mensagem="teste", valor=1000, aliquota=18, resultado=180.0,
        caminho=banco_temporario,
    )

    historico = listar_calculos(banco_temporario)

    assert len(historico) == 1
    assert historico[0]["resultado"] == 180.0
