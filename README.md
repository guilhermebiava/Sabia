# 🐦 Sabiá – Assistente Virtual Universitário

Sabiá é um assistente virtual desenvolvido para auxiliar estudantes e professores da **UTFPR** com informações institucionais como regulamentos, documentos e outros conteúdos relevantes — de forma **rápida, simples e inteligente**.

---

## 🌱 Por que “Sabiá”?

O **sabiá-laranjeira** é a ave símbolo do Paraná, famosa pelo seu canto harmonioso e presença marcante na fauna brasileira. Assim como a ave, nosso assistente busca **comunicar-se de forma clara e eficiente**, promovendo o conhecimento de forma acessível para toda a comunidade acadêmica.

---

## 🚀 Sobre o Projeto

Este projeto foi criado para ser:

✅ **Fácil de implementar**  
🎨 **Altamente personalizável**  
🏫 **Adaptável a qualquer universidade ou instituição**

Você pode:

- Personalizar o comportamento do assistente
- Adaptar o visual da interface
- Treinar o modelo com documentos da sua universidade

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
├── 📁 __pycache__/           # Arquivos temporários do Python
├── 📁 .vscode/               # Configurações do VS Code (opcional)
├── 📁 db/                    # Banco vetorial (ChromaDB)
├── 📁 pdfs/                  # Coloque aqui os PDFs da universidade
├── 📁 venv/                  # Ambiente virtual (não versionar)
│
├── app.py                   # Interface principal com Streamlit
├── config.py                # Armazena as chaves da API
├── ingest.py                # Processamento e embeddings dos PDFs
├── prompt.py                # Personalização do comportamento da IA
├── rag.py                   # Lógica principal de resposta RAG
├── requirements.txt         # Dependências do projeto
├── README.md                # Este arquivo
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
.env\Scriptsctivate   # Windows
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

## 🧩 Personalização

### 🎨 Interface – `app.py`
Você pode personalizar:
- Nome da página (`st.set_page_config`)
- Ícones e cores
- Títulos, mensagens e placeholders

### 🧠 Comportamento da IA – `prompt.py`
Altere o template para definir:
- Tom de voz (formal, casual, divertido...)
- Persona (ex: professor, colega de classe, bot neutro...)

### 🤖 Resposta da IA – `rag.py`

A função `gerar_resposta()` pode ser customizada nos pontos abaixo:

```python
context = db.similarity_search_with_relevance_scores(user_query, k=3)  # 🔢 Número de documentos considerados
context = list(filter(lambda x: x[1] >= 0.5, context))                 # 🎯 Threshold de relevância
modelo = "gpt-4o-mini"                                                 # 🤖 Modelo utilizado (ex: gpt-3.5, mixtral...)
```

Você pode:
- Alterar o número de documentos (`k`)
- Ajustar a pontuação mínima de relevância
- Trocar o modelo por outro disponível no OpenRouter ou OpenAI

---

## 🔐 Autenticação

### 🗝️ OpenRouter
Crie uma conta e gere sua chave em: https://openrouter.ai  
Adicione a chave no `config.py`

### 🗝️ OpenAI
Para embeddings ou uso de modelos da OpenAI, gere sua chave em: https://platform.openai.com  
Também adicione no `config.py`

---

## ✨ Adapte Como Quiser!

O Sabiá é flexível! Você pode:

- Substituir o modelo por outro (Claude, Mixtral, Gemini etc.)
- Usar outro vetorstore (FAISS, Pinecone, etc.)
- Integrar com sistemas internos da universidade

---

## 🤝 Contribuindo

Achou útil? Quer adaptar para sua instituição?  
**Fique à vontade!** Basta criar um fork, modificar o que quiser e voar com o Sabiá 🐤

---

## 📬 Contato

Dúvidas, ideias ou sugestões?  
Abra uma *issue* ou mande uma mensagem por aqui mesmo no GitHub.

---

**Feito com 💚 por e para a comunidade acadêmica.**
