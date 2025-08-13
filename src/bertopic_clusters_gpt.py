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

    Com base na informação acima, extrai um rótulo de tópico curto, mas altamente descritivo, de no máximo 5 palavras. Certifica-te de que está no seguinte formato:
    tópico: <rótulo tópico>
    """
        
    # best practices for BERTopic
    embedding_model = SentenceTransformer("PORTULAN/serafim-900m-portuguese-pt-sentence-encoder")
    umap_model = UMAP(n_neighbors=8, n_components=5, min_dist=0.0, metric='cosine', random_state=42) # try with pca as well
    hdbscan_model = HDBSCAN(min_cluster_size=min_cluster_size, metric='euclidean', cluster_selection_method='eom', prediction_data=True) # try with kmeans as well
    vectorizer_model = CountVectorizer(stop_words=portuguese_stopwords, min_df=2, ngram_range=(1, 2))
    ctfidf_model = ClassTfidfTransformer(bm25_weighting=True)
    
    keybert_model = KeyBERTInspired()
    pos_model = PartOfSpeech("pt_core_news_lg")
    mmr_model = MaximalMarginalRelevance(diversity=0.3)
    client = openai.OpenAI(api_key=OPENAI_KEY)
    openai_model = OpenAI(client, model="gpt-5", exponential_backoff=True, prompt=prompt)

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
    
    chatgpt_topic_labels = {topic: " | ".join(list(zip(*values))[0]) for topic, values in topic_model.topic_aspects_["OpenAI"].items()}
    chatgpt_topic_labels[-1] = "Outlier Topic"
    topic_model.set_topic_labels(chatgpt_topic_labels)
    
    os.makedirs(f"data/adhd-beliefs-pt/bertopic_models/{folder_name}/", exist_ok=True)
    topic_model.save(f"data/adhd-beliefs-pt/bertopic_models/{folder_name}/", serialization="safetensors", save_ctfidf=True, save_embedding_model=embedding_model)
    return df, topic_model, topics, probs

def preprocess_data(df):
    question_types = ["special_interest", "diary_entry", "selfdefining_memory", "empty_sheet"]
    topic_df = pd.concat([df.assign(question=q) for q in question_types], ignore_index=False)
    topic_df["response"] = topic_df.apply(lambda row: row[row["question"]], axis=1)
    topic_df["response_embedding"] = topic_df.apply(lambda row: row[f"{row['question']}_embedding"], axis=1)
    topic_df = topic_df.drop(columns=["special_interest", "diary_entry", "selfdefining_memory", "empty_sheet", "merged_text", "special_interest_embedding", "diary_entry_embedding", "selfdefining_memory_embedding", "empty_sheet_embedding", "merged_text_embedding"])
    topic_df = topic_df.dropna(subset=["response"])
    question_counts = topic_df["question"].value_counts()
    logging.info(f"Question counts:\n{question_counts}")
    topic_df['group'] = (
        topic_df['sex'].map({'Feminino':'Female','Masculino':'Male'}).astype(str) + '_' +
        np.where(topic_df['adhd_diagnosis']=="Sim, diagnosticado", 'ADHD', 'noADHD')
    )
    return topic_df

def main():
    # === Force CUDA and GPU config ===
    assert torch.cuda.is_available(), "No GPU detected!"
    device_id = 1 
    torch.cuda.set_device(device_id) 
    device = f"cuda:{device_id}"
    logging.info(f"Using device: {device}")
    
    
    logging.info("Starting data preprocessing...")
    df = pd.read_pickle("data/adhd-beliefs-pt/adhd-beliefs-pt-embeddings-serafim.pkl")
    topic_df = preprocess_data(df)
    logging.info("Data preprocessing completed.")
    logging.info(f"Data loaded with {len(topic_df)} rows and {len(topic_df.columns)} columns.")

    logging.info("Starting BERTopic clustering...")
    
    column = "response"
    df_women_adhd = topic_df[topic_df["group"] == "Female_ADHD"]
    df_others = topic_df[topic_df["group"] != "Female_ADHD"]
    df_women_noadhd = topic_df[topic_df["group"] == "Female_noADHD"]
    df_men_adhd = topic_df[topic_df["group"] == "Male_ADHD"]
    df_men_noadhd = topic_df[topic_df["group"] == "Male_noADHD"]
    df_women = topic_df[topic_df["group"].isin(["Female_ADHD", "Female_noADHD"])]
    df_men = topic_df[topic_df["group"].isin(["Male_ADHD", "Male_noADHD"])]

    group_names = [
        "Female_ADHD",
        "Others",
        "Female_noADHD",
        "Male_ADHD",
        "Male_noADHD",
        "Female",
        "Male"
    ]
    dfs = [df_women_adhd, df_others, df_women_noadhd, df_men_adhd, df_men_noadhd, df_women, df_men]
    for df_group, group_name in zip(dfs, group_names):
        time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        texts = df_group[column].tolist()
        embeddings = np.vstack(df_group[f"{column}_embedding"])
        folder_name = f"{group_name}_{time}"
        df_group, topic_model, topics, probs = run_bertopic_model(df_group, texts, embeddings, folder_name, min_cluster_size=2)
        logging.info(f"Topics found for {group_name}: {len(set(topics))}")
        logging.info(f"Valid topic documents: {len(df_group[df_group['topic'] != -1])} of {len(df_group)}")
        logging.info(f"Finished BERTopic clustering for {group_name}.")

if __name__ == "__main__":
    logging.info("Starting")
    main()
    logging.info("BERTopic clustering completed successfully.")

