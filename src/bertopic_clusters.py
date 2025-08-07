from bertopic import BERTopic
import numpy as np
import pandas as pd
from transformers import pipeline
from bertopic.representation import TextGeneration
from bertopic.vectorizers import ClassTfidfTransformer
from sentence_transformers import SentenceTransformer
import seaborn as sns
import matplotlib.pyplot as plt
import torch
import datetime
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_bertopic_model(df, model, text_column, embedding_column, min_topic_size=5):
    df = df.dropna(subset=text_column)
    texts = df[text_column].tolist()
    embeddings = np.vstack(df.loc[df[text_column].notna(), embedding_column])

    prompt = """
    Tens acesso ao seguinte conjunto de documentos de participantes:

    [DOCUMENTS]

    Estas respostas partilham um tema comum, que pode ser descrito pelas seguintes palavras-chave:

    [KEYWORDS]

    Com base nesta informação, gera um título curto e representativo para este tema.

    O título deve:
    - Ser claro, direto e conciso (máximo 4 palavras)
    - Refletir com precisão o conteúdo dos documentos
    - Estar escrito em português europeu

    Importante: devolve apenas o título e nada mais.
    Não incluas explicações, descrições ou frases completas.
    Se não conseguires identificar um tema claro, responde apenas com: Tema desconhecido
    """
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logging.info(f"Using device: {device}")

    access_token = "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"

    generator = pipeline(
        "text-generation",
        model=model,
        device=device,
        torch_dtype=torch.float16 if torch.cuda.is_available() else "auto",
	    token=access_token,
    )
    
    representation_model = TextGeneration(generator, prompt=prompt)
    embedding_model = SentenceTransformer("PORTULAN/serafim-900m-portuguese-pt-sentence-encoder")
    ctfidf_model = ClassTfidfTransformer(bm25_weighting=True, reduce_frequent_words=True)

    topic_model = BERTopic(
        representation_model=representation_model,
        embedding_model=embedding_model,
        language="multilingual",
        min_topic_size=min_topic_size,
        verbose=True,
        calculate_probabilities=True,
        ctfidf_model=ctfidf_model,
    )

    topics, probs = topic_model.fit_transform(texts, embeddings)
    df["topic"] = topics
    return df, topic_model, topics, probs

def get_topics(df, topic_model, column, output_file=None):
    lines = []
    # Loop through each topic (excluding outliers)
    for topic in sorted(df["topic"].unique()):
        if topic == -1:
            continue

        topic_label = topic_model.get_topic_info().set_index("Topic").loc[topic]["Name"]
        texts_in_topic = df[df["topic"] == topic][column]

        lines.append(f"\n\n🧠 Topic {topic}: {topic_label}")
        lines.append(f"Total documents: {len(texts_in_topic)}")
        lines.append("-" * 60)

        for idx, text in enumerate(texts_in_topic, 1):
            lines.append(f"{idx}. {text}\n")

    output = "\n".join(lines)
    if output_file:
        logging.info(f"Writing topics to {output_file}")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        logging.info("Output file not specified, printing topics to console.")
        logging.info(output)



def main():
    columns = [
        "special_interest",
        "diary_entry",
        "selfdefining_memory",
        "empty_sheet"
    ]
    
    logging.info("Starting BERTopic clustering...")
    # === Force CUDA and GPU config ===
    assert torch.cuda.is_available(), "No GPU detected!"
    device_id = 1 
    torch.cuda.set_device(device_id) 
    device = f"cuda:{device_id}"
    logging.info(f"Using device: {device}")

    time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    df = pd.read_pickle("data/adhd-beliefs-pt/adhd-beliefs-pt-embeddings-serafim.pkl")
    logging.info(f"Data loaded with {len(df)} rows and {len(df.columns)} columns.")

    model = "mistralai/Magistral-Small-2506"
    model_id = model.split("/")[-1]

    for column in columns:
        logging.info(f"\n\nRunning BERTopic for column: {column}")
        df_copy = df.copy()
        mask_women_adhd = (df['sex']=="Feminino") & (df['adhd_diagnosis']=="Sim, diagnosticado")
        mask_others = ~mask_women_adhd
        df_women_adhd = df_copy[mask_women_adhd]
        df_others = df_copy[mask_others]
        
        logging.info(f"Running {column} for Women with ADHD")
        df_women_adhd, topic_model, topics, probs = run_bertopic_model(df_women_adhd, model, column, f"{column}_embedding", min_topic_size=2)
        valid_docs = df_women_adhd[df_women_adhd["topic"] != -1]
        logging.info(f"Valid topic documents: {len(valid_docs)} of {len(df_women_adhd)}")
        get_topics(df_women_adhd, topic_model, column, f"src/outputs/{time}_bertopic_{column}_{model_id}_women_adhd.txt")
        logging.info("\n\n" + "="*80 + "\n\n")
        
        logging.info(f"Running {column} for Others")
        df_others, topic_model, topics, probs = run_bertopic_model(df_others, model, column, f"{column}_embedding", min_topic_size=2)
        valid_docs = df_others[df_others["topic"] != -1]
        logging.info(f"Valid topic documents: {len(valid_docs)} of {len(df_others)}")
        get_topics(df_others, topic_model, column, f"src/outputs/{time}_bertopic_{column}_{model_id}_others.txt")
        logging.info("\n\n" + "="*80 + "\n\n")

if __name__ == "__main__":
    print("starting")
    logging.info("starting")
    main()
    logging.info("BERTopic clustering completed successfully.")

