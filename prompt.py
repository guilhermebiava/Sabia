from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("""
Answer the user query based on context. If you dont't know the answer or the context do not have the answer, say that you don't know.
ALWAYS answer in pt-BR. You are going to answer questions about documents. Supose you're a waiter.

## CONTEXT
{contexto}

## USER QUERY
{pergunta}
""")
