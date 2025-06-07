from ingest import carregar_documentos, gerar_chunks, criar_vetores
from rag import gerar_resposta
import os
import pandas as pd
import time

perguntas = [
    "O que é o jubilamento?"
]

modelos_llm = {
    'GPT 4o': 'gpt-4o-mini',
    'DeepSeek R1': 'deepseek/deepseek-r1-0528-qwen3-8b:free',
    'LLama 4 Scout': 'meta-llama/llama-4-scout:free',
    'Gemini 2.0 Flash': 'google/gemini-2.0-flash-exp:free',
    "Gemma 3n": 'google/gemma-3n-e4b-it:free',
    "Qwen3-235b": "qwen/qwen3-235b-a22b:free",
}

print("Carregando documentos e criando vetores...")
documentos = carregar_documentos()
chunks = gerar_chunks(documentos)
db = criar_vetores(chunks)

resultados = []

for i, pergunta in enumerate(perguntas, 1):
    print(f"\n==> Pergunta {i}: {pergunta}")
    linha = {"Pergunta": pergunta}
    for nome_modelo, id_modelo in modelos_llm.items():
        try:
            start = time.time()
            resposta = gerar_resposta(pergunta, db, modelo=id_modelo)
            end = time.time()
        except Exception as e:
            resposta = f"[Erro: {e}]"
            end = time.time()
        print(f"{nome_modelo}: {resposta[:60]}...")
        linha[nome_modelo] = resposta
        linha[f"{nome_modelo} (s)"] = round(end - start, 2)
    resultados.append(linha)

df = pd.DataFrame(resultados)
output_path = "resultados_modelos.xlsx"
df.to_excel(output_path, index=False)

print(f"\nTodas as respostas foram salvas em: {output_path}")