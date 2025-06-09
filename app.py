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

st.markdown('<div class="centered-header">Sabiá - Assistente Virtual Universitário</div>', unsafe_allow_html=True)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'models_generation' not in st.session_state:
    st.session_state['models_generation'] = []

if not dbCarregado:
    documentos = carregar_documentos()
    chunks = gerar_chunks(documentos)
    db = criar_vetores(chunks)

# Adiciona seleção de modelo LLM na barra lateral
modelos_llm = {
    'DeepSeek R1': 'deepseek/deepseek-r1-0528-qwen3-8b:free',
    'LLama 4 Scout': 'meta-llama/llama-4-scout:free',
    'GPT 4o': 'gpt-4o-mini',
    'Gemini 2.0 Flash': 'google/gemini-2.0-flash-exp:free',
    "Gemma 3n": 'google/gemma-3n-e4b-it:free',
    "Phy 4": "microsoft/phi-4-reasoning:free",
    "Qwen3-235b": "qwen/qwen3-235b-a22b:free",

}

modelo_escolhido = st.sidebar.selectbox(
    'Escolha o modelo LLM:',
    list(modelos_llm.keys()),
    index=0
)

def get_text():
    input_text = st.chat_input("Como eu posso ajudar hoje?")
    return input_text 

user_input = get_text()

if user_input:
    # Passa o modelo escolhido para a função gerar_resposta
    output = gerar_resposta(user_input, db, modelo=modelos_llm[modelo_escolhido])
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)
    st.session_state.models_generation.append(modelo_escolhido)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])):
        st.markdown(
            f"""
            <div style='display: flex; justify-content: flex-end; margin-bottom: 0.8em;'>
                <div style='display: flex; align-items: center;'>
                    <div style='margin-right: 8px; background: #e6e6e6; border-radius: 8px; padding: 6px 10px; font-size: 1em; text-align: right;'>{st.session_state['past'][i]}</div>
                    <span style='font-size:1.3em;'>{'👨‍💻'}</span>
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
                    <div style='margin-left: 8px; background: #f0f0ff; border-radius: 8px; padding: 6px 10px; font-size: 1em; text-align: left;'>
                        {st.session_state['generated'][i]}
                        <p style="margin: 8px 0px; font-size: 0.6em; text-align: right"> Texto gerado por: <b>{st.session_state['models_generation'][i]}</b></p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )