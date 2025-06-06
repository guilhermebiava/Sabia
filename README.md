python -m venv venv

.\venv\Scripts\activate

pip install -r requirements.txt

set OPENAI_API_KEY=sua-chave-aqui

python main.py

🐦 Sabiá – Assistente Virtual Universitário
Sabiá é um assistente virtual feito para auxiliar estudantes e professores da UTFPR com informações sobre regulamentos, documentos e outros conteúdos institucionais, de forma simples e inteligente.

🌱 Por que “Sabiá”?
O sabiá-laranjeira é a ave símbolo do Paraná, conhecida por seu canto melodioso e presença marcante na fauna brasileira. Assim como a ave, nosso assistente tem como missão comunicar-se de forma clara e eficiente, trazendo conhecimento para quem precisa, quando precisa.

🚀 Sobre o Projeto
Este projeto foi desenvolvido com foco em facilidade de implementação e personalização. Você pode:

Personalizar o comportamento do assistente

Adaptar o visual da interface

Treinar o modelo com os documentos da sua própria universidade

Perfeito para outras instituições que desejam criar seu próprio IA acadêmico! 💡

⚙️ Tecnologias Utilizadas
🐍 Python 3.9

🖥️ Streamlit – Interface interativa

🧠 OpenRouter – Acesso a múltiplos modelos de linguagem

🧩 ChromaDB – Armazenamento vetorial

🔍 OpenAI Embeddings

🔧 LangChain

📁 Estrutura do Projeto
📂 Sabia/
│
├── 📁 __pycache__/           # Arquivos temporários gerados automaticamente pelo Python
├── 📁 .vscode/               # Configurações do editor VS Code (opcional)
├── 📁 db/                    # Armazena o banco vetorial (ChromaDB)
├── 📁 pdfs/                  # Coloque aqui os documentos da universidade para o treinamento
├── 📁 venv/                  # Ambiente virtual (não incluir no versionamento)
│
├── app.py                   # Interface principal com Streamlit
├── config.py                # Onde você define suas chaves de API
├── ingest.py                # Script para processar os PDFs e gerar embeddings
├── prompt.py                # Define a personalidade e comportamento do assistente
├── rag.py                   # Lógica principal de Resposta com Recuperação (RAG)
├── requirements.txt         # Lista de dependências do projeto
├── readme.txt               # (Substitua por README.md se quiser mostrar bonito no GitHub

🛠️ Como Rodar Localmente
Clone o repositório:
    git clone https://github.com/seu-usuario/projeto-sabia.git
    cd projeto-sabia
    git checkout -b minha-versao-sabia

Crie o ambiente virtual:
    python -m venv venv
    .\venv\Scripts\activate

Instale as dependências:
    pip install -r requirements.txt

Crie o arquivo config.py com o seguinte conteúdo:
    OPENROUTER_API_KEY = "sua-chave-openrouter-aqui"
    OPENAI_API_KEY = "sua-chave-openai-aqui"

Inicie o app:
    streamlit run app.py

🧠 Treinando o Modelo com Seus Documentos
    1. Coloque regulamentos, manuais e documentos da sua universidade na pasta /pdfs.
    2. Eles serão usados para criar os embeddings e alimentar a IA com informações reais.

🧩 Personalização
🎨 Interface (app.py)
Você pode personalizar:
    1. Nome da página (st.set_page_config)
    2. Ícones e cores
    3. Títulos, placeholders, mensagens

🧠 Comportamento da IA (prompt.py)
Edite o template.py para mudar:
    Tom da resposta (formal, amigável, engraçado etc.)
    Persona (assistente institucional, colega de sala, professor etc.)

🤖 RAG (rag.py)
A função gerar_resposta() pode ser ajustada nos seguintes pontos:
context = db.similarity_search_with_relevance_scores(user_query, k=3)  # 🔢 Altere o valor de 'k' para mais ou menos documentos
context = list(filter(lambda x: x[1] >= 0.5, context))                 # 🎯 Ajuste o threshold de relevância
modelo="gpt-4o-mini"                                                   # 🤖 Troque o modelo (gpt-3.5-turbo, mixtral, etc.)

🔐 Autenticação
🔑 OpenRouter
Crie sua chave aqui e adicione em config.py.

🔑 OpenAI (para embeddings ou modelos da OpenAI)
Crie sua chave aqui e adicione em config.py.


✨ Adapte como Quiser!
O Sabiá foi criado pensando em flexibilidade. Você pode:

Usar outra base vetorial (Pinecone, FAISS...)

Substituir o modelo por outro (Claude, Mixtral, etc.)

Integrar com sistemas internos da universidade

🤝 Contribuindo
Achou útil? Quer adaptar para sua universidade? Fique à vontade! Basta criar um fork e começar a voar com o Sabiá 🐤

📬 Contato
Dúvidas, ideias ou sugestões? Mande uma mensagem ou abra uma issue!