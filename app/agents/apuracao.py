import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

#python puro
def calcular_icms(valor: float, aliquota: float) -> float:
    """
    Calculo determinístico, sem LLM. auditavel e testavel isoladamente
    """
    return round(valor * (aliquota / 100), 2)

# descrição da ferramenta para o claude 

TOOLS = [
    {
        "name": "calcular_icms",
        "description": "Calcula o valor do ICMS dado um valor de venda e uma alíquota em porcentagem.",
        "input_schema": {
            "type": "object",
            "properties": {
                "valor": {"type": "number", "description": "Valor da venda em reais"},
                "aliquota": {"type": "number", "description": "Alíquota do ICMS em porcentagem, ex: 18 para 18%"},
            },
            "required": ["valor", "aliquota"],
        },
    }
]

def agente_apuracao(mensagem: str) -> str:
    """
    Agente de apuração fiscal.
    Envia mensagem ao claude com a ferramenta de calculo Disponível.
    se o modelo pedir a ferramenta, executamos e devolvemos o resultado.
    para o modelo formular a resposta final.
    """

    resposta = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=500,
        tools=TOOLS,
        messages=[{"role" : "user", "content": mensagem}]
    )

    # Se o modelo não pediu nenhuma ferramenta, devolvemos o texto direto
    if resposta.stop_reason != "tool_use":
        return _extrair_texto(resposta)

    #Encontramos o bloco de tool_use na resposta
    bloco_tool = next(b for b in resposta.content if b.type == "tool_use")

    if bloco_tool.name == "calcular_icms":
        resultado = calcular_icms(**bloco_tool.input)
    else:
        resultado = "ferramenta desconhecida"

    # Manda o resultado de volta pro modelo formular a resposta final
    resposta_final = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=500,
        messages=[
            {"role": "user", "content": mensagem},
            {"role": "assistant", "content": resposta.content},
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": bloco_tool.id,
                        "content": str(resultado)
                    }
                ], 
            },
        ],
    )
    return _extrair_texto(resposta_final)

def _extrair_texto(resposta) -> str:
    """Extrair o texto de uma resposta da API (pode ter múltiplos blocos)"""
    return "".join(b.text for b in resposta.content if b.type =="text")

