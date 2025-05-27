import streamlit as st
from streamlit_chat import message
import requests
from ingest import carregar_documentos, gerar_chunks, criar_vetores
from rag import gerar_resposta
import streamlit as st
from st_chat_message import message

dbCarregado = False

st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)

#API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
#headers = {"Authorization": st.secrets['api_key']}

st.header("Sabiá - Assistente Virtual")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if not dbCarregado:
    documentos = carregar_documentos()
    chunks = gerar_chunks(documentos)
    db = criar_vetores(chunks)

##	response = requests.post(API_URL, headers=headers, json=payload)
#	return payload

def get_text():
    #input_text = st.text_input("You: ","", key="input")
    input_text = st.chat_input("Como eu posso ajudar hoje?")
    return input_text 

user_input = get_text()

if user_input:
    output = gerar_resposta(user_input, db)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))
