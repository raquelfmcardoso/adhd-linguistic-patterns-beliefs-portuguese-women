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
import nltk
from nltk.corpus import stopwords
import logging
import os
from dotenv import load_dotenv
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import openai
import spacy
from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance, OpenAI, PartOfSpeech

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
nltk.download("stopwords", quiet=True)
portuguese_stopwords = stopwords.words("portuguese")
additional_stopwords = [
    "pra",
    "pro",
    "tá",
    "já",
    "ter",
    "vai",
    "vou",
    "então",
    "assim",
    "aí",
    "sobre"
]
portuguese_stopwords.extend(additional_stopwords)

def run_bertopic_model(df, texts, embeddings, output_dir, min_cluster_size=5):
    time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    prompt = """
    Eu tenho um tópico que contem o seguinte conjunto de documentos:
    [DOCUMENTS]
    O tópico é descrito pelas seguintes palavras-chave: [KEYWORDS]

    Com base na informação acima, extrai um rótulo de tópico curto, mas altamente descritivo, de no máximo 5 palavras.
    Escreve-o em Inglês e certifica-te de que está no seguinte formato:
    topic: <topic label>
    """
        
    # best practices for BERTopic
    embedding_model = SentenceTransformer("PORTULAN/serafim-900m-portuguese-pt-sentence-encoder")
    umap_model = UMAP(n_neighbors=5, n_components=5, min_dist=0.0, metric='cosine', random_state=42) # try with pca as well
    hdbscan_model = HDBSCAN(min_cluster_size=min_cluster_size, metric='euclidean', cluster_selection_method='eom', prediction_data=True) # try with kmeans as well
    vectorizer_model = CountVectorizer(stop_words=portuguese_stopwords, min_df=2, ngram_range=(1, 2))
    ctfidf_model = ClassTfidfTransformer(bm25_weighting=True)
    
    keybert_model = KeyBERTInspired()
    pos_model = PartOfSpeech("pt_core_news_lg")
    mmr_model = MaximalMarginalRelevance(diversity=0.3)
    client = openai.OpenAI(api_key=OPENAI_KEY)
    openai_model = OpenAI(client, model="gpt-4.1", exponential_backoff=True, prompt=prompt)

    representation_model = {
        "KeyBERT": keybert_model,
        "OpenAI": openai_model,
        "MMR": mmr_model,
        "POS": pos_model,
    }
    
    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        representation_model=representation_model,
        language="multilingual",
        top_n_words=10,
        verbose=True,
        calculate_probabilities=True,
        ctfidf_model=ctfidf_model,
    )

    topics, probs = topic_model.fit_transform(texts, embeddings)
    df["topic"] = topics
    df["probability"] = [probs[i][topic] if topic != -1 else 0.0 for i, topic in enumerate(topics)]
    
    chatgpt_topic_labels = {topic: " | ".join(list(zip(*values))[0]) for topic, values in topic_model.topic_aspects_["OpenAI"].items()}
    chatgpt_topic_labels[-1] = "Outlier Topic"
    topic_model.set_topic_labels(chatgpt_topic_labels)

    os.makedirs(f"{output_dir}/{min_cluster_size}_{time}/", exist_ok=True)
    topic_model.save(f"{output_dir}/{min_cluster_size}_{time}/", serialization="safetensors", save_ctfidf=True, save_embedding_model=embedding_model)
    return df, topic_model, topics, probs

def get_cluster_sizes(group_name):
        """Get the cluster sizes for a specific group name."""
        if group_name == "Female_ADHD":
            return [2, 3, 4, 5, 6, 7, 8, 10]
        elif group_name == "Female_noADHD":
            return [2, 3, 4, 5, 6, 7, 8, 10, 12, 15]
        elif group_name == "ADHD":
            return [2, 3, 4, 5, 6, 7, 8, 10, 12]
        elif group_name == "noADHD":
            return [2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25]
        return [2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25]

def main():
    
    print("Starting data loading...")
    topic_df = pd.read_pickle("data/adhd-beliefs-pt/adhd-beliefs-pt-embeddings-serafim-bertopic.pkl")
    print(f"Data loaded with {len(topic_df)} rows and {len(topic_df.columns)} columns.")
    print("Starting BERTopic clustering...")

    column = "response"
    df_women_adhd = topic_df[topic_df["group"] == "Female_ADHD"]
    df_women_noadhd = topic_df[topic_df["group"] == "Female_noADHD"]
    df_adhd = topic_df[topic_df["group"].isin(["Male_ADHD", "Female_ADHD"])]
    df_noadhd = topic_df[topic_df["group"].isin(["Male_noADHD", "Female_noADHD"])]

    group_names = [
        "Female_ADHD",
        "Female_noADHD",
        "ADHD",
        "noADHD"
    ]

    dfs = [df_women_adhd, df_women_noadhd, df_adhd, df_noadhd]
    for df_group, group_name in zip(dfs, group_names):
        print("=" * 60)
        print(f"Starting BERTopic clustering for {group_name}.")
        texts = df_group[column].tolist()
        embeddings = np.vstack(df_group[f"{column}_embedding"])

        cluster_sizes = get_cluster_sizes(group_name)
        for n in cluster_sizes:
            min_cluster_size = n
            print(f"Group {group_name}: {len(texts)} texts, using min_cluster_size={min_cluster_size}")

            output_dir = f"data/adhd-beliefs-pt/bertopic_tuning/{group_name}/"
            os.makedirs(f"{output_dir}", exist_ok=True)
            existing = [d for d in os.listdir(output_dir) if d.startswith(f"{min_cluster_size}_")]
            if not existing:
                print(f"Running BERTopic model for {group_name} with min_cluster_size={min_cluster_size}.")
                df_group, topic_model, topics, probs = run_bertopic_model(df_group, texts, embeddings, output_dir, min_cluster_size=min_cluster_size)
                print(f"Topics found for {group_name}: {len(set(topics))}")
                print(f"Valid topic documents: {len(df_group[df_group['topic'] != -1])} of {len(df_group)}")
                print(f"Finished BERTopic clustering for {group_name} with min_cluster_size={min_cluster_size}.")
                print("-" * 40)
        print(f"Finished BERTopic clustering for {group_name}.")

if __name__ == "__main__":
    print("Starting")
    main()
    print("BERTopic clustering completed successfully.")

