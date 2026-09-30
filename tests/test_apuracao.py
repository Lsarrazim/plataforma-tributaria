from unittest.mock import patch, MagicMock
from app.agents.apuracao import calcular_icms, agente_apuracao

def test_calcular_icms():
    """testa a função pura de calculo, sem envolver LLM nenhum."""
    assert calcular_icms(1000, 18) == 180.0
    assert calcular_icms(500,10) == 50.0

def _fake_tool_use_response(valor, aliquota):
    """Fixture auxiliar: simula a 1 resposta da API(pedido de ferramenta)"""
    bloco_tool = MagicMock()
    bloco_tool.type = "tool_use"
    bloco_tool.name = "calcular_icms"
    bloco_tool.input = {"valor": valor, "aliquota": aliquota}
    bloco_tool.id = "fake_id_123"

    resposta = MagicMock()
    resposta.stop_reason = "tool_use"
    resposta.content = [bloco_tool]
    return resposta

def _fake_text_response(texto):
    """Fixture auxiliar: simula a 2 resposta da API (texto final)"""
    bloco_texto = MagicMock()
    bloco_texto.type = "text"
    bloco_texto.text = texto

    resposta = MagicMock()
    resposta.content = [bloco_texto]
    return resposta

def test_agente_apuracao_chama_ferramenta_correta():
    """
    testa o fluxo completo do agente sem gastar o crédito de API:
    a chamada real ao claude é substituído por resposta simulada
    """
    with patch("app.agents.apuracao.client.messages.create") as mock_create:
        mock_create.side_effect = [
            _fake_tool_use_response(valor=1000, aliquota=18),
            _fake_text_response("o ICMS é R$ 180,00."),
        ]

        resultado = agente_apuracao("quanto de ICMS eu pago numa venda de 1000 reais?")

        assert "180" in resultado
        assert mock_create.call_count == 2