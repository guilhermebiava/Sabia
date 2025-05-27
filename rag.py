from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from config import OPENAI_API_KEY
from prompt import template

def gerar_resposta(user_query, db):
    context = db.similarity_search_with_relevance_scores(user_query, k=3)
    context = list(filter(lambda x: x[1] >= 0.5, context))

    if not context:
        return "Eu não sou capaz de responder a essa pergunta."

    contexto_formatado = "\n\n".join([
        f"## Documento {k}\n{doc[0].page_content}\nSource: {doc[0].metadata.get('source', '')}"
        for k, doc in enumerate(context, start=1)
    ])

    chain = template | ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY) | StrOutputParser()
    return chain.invoke({"contexto": contexto_formatado, "pergunta": user_query})