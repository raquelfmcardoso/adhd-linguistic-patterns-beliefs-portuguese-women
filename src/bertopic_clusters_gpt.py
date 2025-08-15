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

def run_bertopic_model(df, texts, embeddings, folder_name, min_cluster_size=5):
    
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
    kmeans_model = KMeans(n_clusters=50)
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
    # new_topics = topic_model.reduce_outliers(texts, topics)
    df["topic"] = topics
    df["probability"] = [probs[i][topic] if topic != -1 else 0.0 for i, topic in enumerate(topics)]
    
    chatgpt_topic_labels = {topic: " | ".join(list(zip(*values))[0]) for topic, values in topic_model.topic_aspects_["OpenAI"].items()}
    chatgpt_topic_labels[-1] = "Outlier Topic"
    topic_model.set_topic_labels(chatgpt_topic_labels)
    
    os.makedirs(f"data/adhd-beliefs-pt/bertopic_models/{folder_name}/", exist_ok=True)
    topic_model.save(f"data/adhd-beliefs-pt/bertopic_models/{folder_name}/", serialization="safetensors", save_ctfidf=True, save_embedding_model=embedding_model)
    return df, topic_model, topics, probs

def main():
    # === Force CUDA and GPU config ===
    # assert torch.cuda.is_available(), "No GPU detected!"
    # device_id = 1 
    # torch.cuda.set_device(device_id) 
    # device = f"cuda:{device_id}"
    # logging.info(f"Using device: {device}")
    
    print("Starting data loading...")
    topic_df = pd.read_pickle("data/adhd-beliefs-pt/adhd-beliefs-pt-embeddings-serafim-bertopic.pkl")
    print(f"Data loaded with {len(topic_df)} rows and {len(topic_df.columns)} columns.")
    print("Starting BERTopic clustering...")

    def calculate_min_cluster_size(num_texts):
        """Calculate min_cluster_size based on actual group sizes in the dataset"""
        if num_texts <= 30:
            return 2  # Very small groups (≤30): minimum viable clusters
        elif num_texts <= 70:
            return 2  # Small groups (31-60): allow for 3-4 clusters
        elif num_texts <= 120:
            return 2  # Medium-small groups (61-120): allow for 4-6 clusters  
        elif num_texts <= 250:
            return 4  # Medium groups (121-250): allow for 5-10 clusters
        else:
            return 5  # Large groups (250+): scale appropriately
    
    column = "response"
    df_women_adhd = topic_df[topic_df["group"] == "Female_ADHD"]
    df_others = topic_df[topic_df["group"] != "Female_ADHD"]
    df_women_noadhd = topic_df[topic_df["group"] == "Female_noADHD"]
    df_men_adhd = topic_df[topic_df["group"] == "Male_ADHD"]
    df_men_noadhd = topic_df[topic_df["group"] == "Male_noADHD"]
    df_women = topic_df[topic_df["group"].isin(["Female_ADHD", "Female_noADHD"])]
    df_men = topic_df[topic_df["group"].isin(["Male_ADHD", "Male_noADHD"])]
    df_all = topic_df

    group_names = [
        "Female_ADHD",
        "Others",
        "Female_noADHD",
        "Male_ADHD",
        "Male_noADHD",
        "Female",
        "Male",
        "All"
    ]
    
    dfs = [df_women_adhd, df_others, df_women_noadhd, df_men_adhd, df_men_noadhd, df_women, df_men, df_all]
    time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    for df_group, group_name in zip(dfs, group_names):
        print("=" * 60)
        print(f"Starting BERTopic clustering for {group_name}.")
        texts = df_group[column].tolist()
        embeddings = np.vstack(df_group[f"{column}_embedding"])
        
        # Calculate adaptive min_cluster_size based on group size
        adaptive_min_cluster_size = calculate_min_cluster_size(len(texts))
        print(f"Group {group_name}: {len(texts)} texts, using min_cluster_size={adaptive_min_cluster_size}")
        
        folder_name = f"{group_name}_{time}_2"
        df_group, topic_model, topics, probs = run_bertopic_model(df_group, texts, embeddings, folder_name, min_cluster_size=adaptive_min_cluster_size)
        os.makedirs(f"data/adhd-beliefs-pt/bertopic_dfs/", exist_ok=True)
        df_group.to_pickle(f"data/adhd-beliefs-pt/bertopic_dfs/{folder_name}.pkl")

        print(f"Topics found for {group_name}: {len(set(topics))}")
        print(f"Valid topic documents: {len(df_group[df_group['topic'] != -1])} of {len(df_group)}")
        print(f"Finished BERTopic clustering for {group_name}.")

if __name__ == "__main__":
    print("Starting")
    main()
    print("BERTopic clustering completed successfully.")

