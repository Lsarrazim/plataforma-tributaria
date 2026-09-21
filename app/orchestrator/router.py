from app.agents.apuracao import agente_apuracao

AGENTES = {
    "apuracao" : agente_apuracao,
}

def escolher_agente(mensagem: str) -> str:

    """"decidi qual agente deve tratar a mensagem"""
    return "apuracao"


def orquestrar(mensagem: str) -> str:

    """ponto de entrada único: recebe a mensagem, roteia, devolve a resposta."""

    nome_agente = escolher_agente(mensagem)
    agente = AGENTES[nome_agente]
    return agente(mensagem)