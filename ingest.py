from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from config import OPENAI_API_KEY
import os

def carregar_documentos():
    pasta_pdfs = os.path.join(os.getcwd(), "pdfs")
    documentos = []
    for nome_arquivo in os.listdir(pasta_pdfs):
        if nome_arquivo.lower().endswith(".pdf"):
            caminho_pdf = os.path.join(pasta_pdfs, nome_arquivo)
            loader = PyPDFLoader(caminho_pdf)
            documentos.extend(loader.load())
    return documentos

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