from app.orchestrator.router import orquestrar

if __name__ == "__main__":
    resposta = orquestrar("quanto de ICMS eu devo pagar numa venda de 1000 reais")
    print(resposta)