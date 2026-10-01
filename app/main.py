from app.orchestrator.router import orquestrar
from app.db.database import criar_tabelas

if __name__ == "__main__":
    criar_tabelas()
    resposta = orquestrar("quanto de ICMS eu devo pagar numa venda de 1000 reais")
    print(resposta)