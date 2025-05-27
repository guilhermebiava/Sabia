import streamlit as st
from streamlit_chat import message
import requests
from ingest import carregar_documentos, gerar_chunks, criar_vetores
from rag import gerar_resposta
from st_chat_message import message

dbCarregado = False

st.set_page_config(
    page_title="Sabiá - Assistente Virtual",
    page_icon="🐦",  
)

st.markdown(
    """
    <style>
    .centered-header {
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 1em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="centered-header">Sabiá - Assistente Virtual da UTFPR</div>', unsafe_allow_html=True)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if not dbCarregado:
    documentos = carregar_documentos()
    chunks = gerar_chunks(documentos)
    db = criar_vetores(chunks)

def get_text():
    input_text = st.chat_input("Como eu posso ajudar hoje?")
    return input_text 

user_input = get_text()

if user_input:
    output = gerar_resposta(user_input, db)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])):
        st.markdown(
            f"""
            <div style='display: flex; justify-content: flex-end; margin-bottom: 0.8em;'>
                <div style='display: flex; align-items: center;'>
                    <div style='margin-right: 8px; background: #e6e6e6; border-radius: 8px; padding: 6px 10px; font-size: 1em; text-align: right;'>{st.session_state['past'][i]}</div>
                    <span style='font-size:1.3em;'>{'🙂'}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div style='display: flex; justify-content: flex-start; margin-bottom: 1.5em;'>
                <div style='display: flex; align-items: center;'>
                    <span style='font-size:1.3em;'>{'🐦'}</span>
                    <div style='margin-left: 8px; background: #f0f0ff; border-radius: 8px; padding: 6px 10px; font-size: 1em; text-align: left;'>{st.session_state['generated'][i]}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )