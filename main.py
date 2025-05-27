from ingest import carregar_documentos, gerar_chunks, criar_vetores
from rag import gerar_resposta
import streamlit as st
from st_chat_message import message

msg1 = 
msg2 =





st.title("Chat placeholder")

chat_placeholder = st.empty()

with chat_placeholder.container():    
    for i in range(len(st.session_state['generated'])):                
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
        message(
            st.session_state['generated'][i]['data'], 
            key=f"{i}", 
            allow_html=True,
            is_table=True if st.session_state['generated'][i]['type']=='table' else False
        )
    
    st.button("Clear")







if "msgs" not in st.session_state:
    st.session_state.msgs = [{
        "content": "Olá! Eu sou o Sabiá, um assistente virtual. Como posso ajudar você hoje?",
        "is_user": True,
    }]

for idx, msg in enumerate(st.session_state.msgs):
    message(msg["content"], is_user=msg["is_user"], key=f"message_{idx}")

def main():
    documentos = carregar_documentos()
    chunks = gerar_chunks(documentos)
    db = criar_vetores(chunks)

    while True:
        pergunta = input("Usuário: ")
        if pergunta.strip().upper() == "SAIR":
            print("Encerrando o programa.")
            break
        resposta = gerar_resposta(pergunta, db)
        print("Sabiá: " + resposta)

if __name__ == "__main__":
    main()
