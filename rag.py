from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from config import OPENAI_API_KEY, OPENROUTER_API_KEY
from prompt import template
from openai import OpenAI

def gerar_resposta(user_query, db, modelo="gpt-4o-mini"):
    context = db.similarity_search_with_relevance_scores(user_query, k=3)
    context = list(filter(lambda x: x[1] >= 0.5, context))

    if not context:
        return "Eu não sou capaz de responder a essa pergunta."

    contexto_formatado = "\n\n".join([
        f"## Documento {k}\n{doc[0].page_content}\nSource: {doc[0].metadata.get('source', '')}"
        for k, doc in enumerate(context, start=1)
    ])

    # Seleção do modelo e chave apropriada
    if modelo.startswith("gpt"):
        chain = template | ChatOpenAI(model=modelo, temperature=0, api_key=OPENAI_API_KEY) | StrOutputParser()
        return chain.invoke({"contexto": contexto_formatado, "pergunta": user_query})

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    )

    completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    model=modelo,
    messages=[
        {
        "role": "user",
        "content": f"Contexto:\n{contexto_formatado}\n\nPergunta: {user_query}"
        }
    ]
    )

    return completion.choices[0].message.content