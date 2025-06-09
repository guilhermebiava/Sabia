import pandas as pd
from rouge import Rouge
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from sentence_transformers import SentenceTransformer, util
import numpy as np
import argparse
import nltk
import re

# Função para calcular métricas ROUGE e BLEU

def calcular_metricas(csv_path, referencia_col, modelo_cols):
    # Garante que o wordnet está disponível para o METEOR
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')
    print(f"Lendo o arquivo CSV: {csv_path}")
    # Tenta ler o CSV com encoding utf-8, se falhar tenta latin1
    try:
        df = pd.read_csv(csv_path, encoding='utf-8', sep=None, engine='python')
    except UnicodeDecodeError:
        print("Arquivo não está em UTF-8, tentando com encoding 'latin1'...")
        df = pd.read_csv(csv_path, encoding='latin1', sep=None, engine='python')
    except pd.errors.ParserError as e:
        print(f"Erro de parsing: {e}\nTentando com sep=';'...")
        try:
            df = pd.read_csv(csv_path, encoding='utf-8', sep=';', engine='python')
        except Exception:
            df = pd.read_csv(csv_path, encoding='latin1', sep=';', engine='python')
    rouge = Rouge()
    smooth = SmoothingFunction().method1
    resultados = {}
    sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    referencias = [limpar_markdown(t) for t in df[referencia_col].astype(str).tolist()]
    print(f"Referências: {len(referencias)}")
    for modelo in modelo_cols:
        hipoteses = [limpar_markdown(t) for t in df[modelo].astype(str).tolist()]
        # Calcula ROUGE para cada par individualmente
        rouge_1_scores = []
        rouge_2_scores = []
        rouge_l_scores = []
        for hyp, ref in zip(hipoteses, referencias):
            score = rouge.get_scores(hyp, ref)[0]
            rouge_1_scores.append(score['rouge-1']['f'])
            rouge_2_scores.append(score['rouge-2']['f'])
            rouge_l_scores.append(score['rouge-l']['f'])
        scores_bleu = [sentence_bleu([ref.split()], hyp.split(), smoothing_function=smooth) for ref, hyp in zip(referencias, hipoteses)]
        emb_refs = sbert_model.encode(referencias, convert_to_tensor=True)
        emb_hyps = sbert_model.encode(hipoteses, convert_to_tensor=True)
        sbert_scores = util.cos_sim(emb_hyps, emb_refs).diagonal().cpu().numpy()
        scores_meteor = [meteor_score([ref.split()], hyp.split()) for ref, hyp in zip(referencias, hipoteses)]
        # LLM-as-a-Judge (agora retorna dict de médias por critério)
        medias_judge, std_judge = avaliar_llm_as_a_judge(referencias, hipoteses)
        
        resultados[modelo] = {
            'ROUGE-1': float(np.mean(rouge_1_scores)),
            'ROUGE-1_std': float(np.std(rouge_1_scores)),
            'ROUGE-2': float(np.mean(rouge_2_scores)),
            'ROUGE-2_std': float(np.std(rouge_2_scores)),
            'ROUGE-L': float(np.mean(rouge_l_scores)),
            'ROUGE-L_std': float(np.std(rouge_l_scores)),
            'BLEU': float(np.mean(scores_bleu)),
            'BLEU_std': float(np.std(scores_bleu)),
            'SBERT': float(np.mean(sbert_scores)),
            'SBERT_std': float(np.std(sbert_scores)),
            'METEOR': float(np.mean(scores_meteor)),
            'METEOR_std': float(np.std(scores_meteor)),
            'LLM-as-a-Judge': medias_judge,
            'LLM-as-a-Judge_std': std_judge
        }
    return resultados

def limpar_markdown(texto):
    # Remove símbolos comuns de formatação Markdown
    texto = re.sub(r'[\*\_\`\#\>\-\=\~\[\]\(\)\!\|\>\+\^\$\%\@]', '', texto)
    texto = re.sub(r'\n+', ' ', texto)  # Remove quebras de linha extras
    texto = re.sub(r'\s+', ' ', texto).strip()  # Remove espaços extras
    return texto

def avaliar_llm_as_a_judge(referencias, hipoteses, modelo_julgador="gpt-4.1-mini", prompt_julgador=None):
    """
    Avalia as respostas dos modelos usando um LLM como juiz (LLM-as-a-Judge).
    Cada hipótese é comparada com a referência e recebe notas de 1 a 5 para cada critério, depois normalizadas para 0 a 1.
    """
    import openai
    from tqdm import tqdm
    from config import OPENAI_API_KEY
    openai.api_key = OPENAI_API_KEY
    criterios = [
        "Relevância",
        "Acurácia",
        "Completude",
        "Clareza",
        "Concisão"
    ]
    if prompt_julgador is None:
        prompt_julgador = (
            "Avalie a resposta do modelo em relação à referência humana usando os critérios abaixo. "
            "Para cada critério, atribua uma nota de 1 (insatisfatório) a 5 (excepcional), apenas o número.\n"
            "Critérios: Relevância, Acurácia, Completude, Clareza, Concisão.\n"
            "\nRubrica:\n"
            "1: Insatisfatório\n2: Parcialmente Satisfatório\n3: Satisfatório\n4: Bom\n5: Excepcional\n"
            "\nReferência:\n{referencia}\n\nResposta do modelo:\n{hipotese}\n\nResponda apenas com 5 números separados por vírgula, na ordem dos critérios. Exemplo: 3,4,2,5,4"
        )
    resultados = []
    for ref, hyp in tqdm(zip(referencias, hipoteses), total=len(referencias)):
        prompt = prompt_julgador.format(referencia=ref, hipotese=hyp)
        try:
            response = openai.chat.completions.create(
                model=modelo_julgador,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=20,
                temperature=0.0
            )
            notas_str = response.choices[0].message.content.strip()
            notas = [float(n.strip()) for n in notas_str.split(",") if n.strip().isdigit()]
            if len(notas) == 5:
                notas_norm = [round((n-1)/4, 3) for n in notas]  # normaliza para 0-1
                resultados.append(notas_norm)
            else:
                resultados.append([None]*5)
        except Exception as e:
            print(f"Erro ao avaliar com LLM-as-a-Judge: {e}")
            resultados.append([None]*5)
    # Calcula médias por critério e geral
    arr = np.array([r for r in resultados if None not in r])
    if len(arr) > 0:
        medias = float(arr.mean())
        std = float(arr.std())
    else:
        medias = None
        std = None
    return medias, std

if __name__ == "__main__":
    referencia_col = 'Resposta esperada'  # Nome da coluna de referência humana
    modelo_cols = ["GPT 4o", "DeepSeek R1", "LLama 4 Scout", "Gemini 2.0 Flash", "Gemma 3n", "Phy 4", "Qwen3-235b" ]
    csv_path = "resultados_modelos.csv"

    resultados = calcular_metricas(csv_path, referencia_col, modelo_cols)
    for modelo, metricas in resultados.items():
        print(f"\nModelo: {modelo}")
        for metrica, valor in metricas.items():
            if valor is None:
                print(f"  {metrica}: N/A")
            else:
                print(f"  {metrica}: {valor:.4f}")