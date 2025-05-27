from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from config import OPENAI_API_KEY

def carregar_documentos():
    texto = """
    Não. O TCC do BES é individual. O projeto pode ser composto por mais de um acadêmico, entretanto as avaliações e a monografia a ser escrita deve ser um trabalho individual a ser supervisionado por um orientador.


    """  # Você pode carregar de arquivo também se preferir
    return [Document(page_content=texto, metadata={"autor": "UTFPR", "source": "www.utfpr.edu.br"})]

def gerar_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=500,
        length_function=len
    )
    return splitter.split_documents(documents)

def criar_vetores(chunks):
    db = Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY),
        persist_directory="db"
    )
    return db
