
# 🐦 Sabiá – Assistente Virtual Universitário

**Feito com 💚 por e para a comunidade acadêmica.**

![#ParaTodosVerem: A imagem consiste na tela da aplicação Sabiá, que consiste na interface dessa aplicação. Na parte superior tem um título "Sabiá - Assistente Virtual". Mais abaixo, tem um exemplo de interação entre o usuário e o chatbot. Alinhado à direita, tem a pergunta do usuário "PERGUNTA" com um emoji de um estudante no computador. Alinhado à esquerda, tem a resposta do chatbot "RESPOSTA" com um emoji que representa um pássaro. Também tem um placeholder no final da resposta que indica o modelo de LLM que gerou a resposta. Mais abaixo, tem um campo para o usuário digitar sua pergunta e interagir com a aplicação, com um placeholder "Como eu posso ajudar hoje?"](assets/estruturaAplicacao.png)

---

## 🌱 Por que “Sabiá”?

O **sabiá** foi escolhido como nome por simbolizar clareza, leveza e comunicação — características ideais para um assistente de IA. Ele representa um guia amigável e inteligente no dia a dia acadêmico, promovendo o conhecimento de forma acessível e empática.

---

## 🚀 Sobre o Projeto

Este projeto foi criado para ser:

✅ **Fácil de implementar**  
🎨 **Personalizável**  
🏫 **Adaptável a qualquer universidade ou instituição**

Você pode:

- Personalizar o comportamento do assistente
- Adaptar o visual da interface
- Treinar o modelo com documentos institucionais da sua escolha

> ✨ Ideal para qualquer instituição que deseje seu próprio assistente acadêmico com IA!

---

## ⚙️ Tecnologias Utilizadas

- 🐍 **Python 3.9**
- 🖥️ **Streamlit** — Interface web interativa
- 🧠 **OpenRouter** — Acesso a múltiplos LLMs
- 🧩 **ChromaDB** — Armazenamento vetorial
- 🔍 **OpenAI Embeddings**
- 🔧 **LangChain**

---

## 📁 Estrutura do Projeto

```
📂 projeto-sabia/
│
├── 📁 __pycache__/           
├── 📁 .vscode/               
├── 📁 db/                    
├── 📁 pdfs/                  
├── 📁 venv/                  
│
├── app.py                   
├── config.py                
├── ingest.py                
├── prompt.py                
├── rag.py                   
├── requirements.txt         
├── README.md                
```

---

## 🛠️ Como Rodar Localmente

### 1️⃣ Clone o repositório:

```bash
git clone https://github.com/seu-usuario/projeto-sabia.git
cd projeto-sabia
git checkout -b minha-versao-sabia
```

### 2️⃣ Crie e ative o ambiente virtual:

```bash
python -m venv venv
.venv\Scripts\activate   # Windows
```

### 3️⃣ Instale as dependências:

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure suas chaves:

Crie o arquivo `config.py` com este conteúdo:

```python
OPENROUTER_API_KEY = "sua-chave-openrouter-aqui"
OPENAI_API_KEY = "sua-chave-openai-aqui"
```

> 🔐 Ambas as chaves são opcionais, dependendo do modelo e embeddings que você quiser usar.

### 5️⃣ Inicie o aplicativo:

```bash
streamlit run app.py
```

---

## 🧠 Treinando o Modelo com Seus Documentos

1. Coloque seus **regulamentos, manuais e documentos institucionais** na pasta `/pdfs`
2. Rode o script `ingest.py` para criar os embeddings com base nesses documentos

---

## 🔍 Arquitetura da Aplicação

> ![#ParaTodosVerem - Diagrama da arquitetura da aplicação]

### 🧩 Como Funciona:

1. O usuário envia uma pergunta pela interface.
2. A pergunta é enviada para o **RAG** (Retrieval-Augmented Generation).
3. O RAG consulta um **banco de dados vetorial** com documentos institucionais previamente particionados em trechos (chunks) e convertidos em embeddings.
4. Após a busca por similaridade, o RAG retorna o **contexto relevante**.
5. Esse contexto é combinado com a pergunta do usuário, formando um **prompt enriquecido**.
6. O prompt é enviado para o modelo LLM (como GPT-4, Claude, etc.) que gera a resposta final.
7. A resposta é devolvida para o usuário pela interface.

---

## 🎨 Personalização

### Interface – `app.py`
Você pode personalizar:
- Nome da página (`st.set_page_config`)
- Ícones e cores
- Títulos, mensagens e placeholders

### Comportamento da IA – `prompt.py`
Altere o template para definir:
- Tom de voz (formal, casual, divertido...)
- Persona (ex: professor, colega de classe, bot neutro...)

### Resposta da IA – `rag.py`

```python
context = db.similarity_search_with_relevance_scores(user_query, k=3)
context = list(filter(lambda x: x[1] >= 0.5, context))
modelo = "gpt-4o-mini"
```

Você pode:
- Alterar o número de documentos considerados (`k`)
- Ajustar a pontuação mínima de relevância (`0.5`)
- Trocar o modelo LLM utilizado

---

## 🔐 Autenticação

### OpenRouter
- Gere uma chave em: https://openrouter.ai

### OpenAI
- Gere uma chave em: https://platform.openai.com

Coloque suas chaves no arquivo `config.py`.

---

## 🤝 Contribuindo

Achou útil? Quer adaptar para sua instituição?  
**Fique à vontade!** Basta criar um fork, modificar o que quiser e voar com o Sabiá 🐤

---

## 📬 Contato

Dúvidas, ideias ou sugestões?  
Abra uma *issue* ou envie uma mensagem pelo GitHub.

---
