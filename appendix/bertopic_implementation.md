The BERTopic pipeline comprises 4 main components—embedding, dimensionality reduction, clustering, and topic representation—which were adapted to the characteristics of our dataset.  

---

**Sentence Embeddings**

Semantic representations of the responses were generated using the Serafim Sentence Encoder. As described in the **Related Work** chapter, Serafim builds on the SBERT architecture to produce sentence-level embeddings that can be compared directly via cosine similarity. This ensured that semantically related responses were positioned close together in vector space, thereby facilitating the discovery of coherent thematic clusters.

---

**Dimensionality Reduction**

Because clustering in high-dimensional spaces is known to be unstable, the embeddings were reduced using **UMAP**, which preserves both local and global structure while projecting the data into a lower-dimensional space. Parameters were set in line with recommended practices for BERTopic:  
`n_neighbors=5`, `n_components=5`, `min_dist=0.0`, and `metric='cosine'`, with the random state fixed for reproducibility.

---

**Clustering**

Clustering was then performed with **HDBSCAN**, a density-based algorithm able to detect clusters of varying size and to treat non-conforming documents as noise points. This choice avoided the need to pre-specify the number of clusters, as required in K-Means (MacQueen, 1967), which prevented the imposition of an artificial topic structure.

However, it required specifying the minimum documents per cluster in order to balance thematic coherence with interpretability (see **Appendix G** MUDAR PARA AQUI UM FICHEIRO DAQUI). In cases where the clustering results produced excessively fragmented topics, we used BERTopic's `reduce_topics` method to merge semantically similar clusters. Outlier documents that could not be assigned to any cluster were placed in a specified invalid cluster (`ID = -1`) and were excluded from subsequent analysis.  

**Table 1** reports the final number of valid documents, topics, and the minimum documents per cluster for each group.

| **Participant Group**           | **Valid Documents** | **Valid Clusters** | **Minimum Documents per Cluster** |
|----------------------------------|--------------------:|-------------------:|----------------------------------:|
| Women with ADHD                  | 59 / 65             | 8                  | 2                                 |
| Women without ADHD               | 183 / 220           | 15                 | 3                                 |
| Participants with ADHD           | 83 / 94             | 13                 | 2                                 |
| Participants without ADHD        | 305 / 353           | 26                 | 3                                 |

#### Table 1. Final number of valid documents, clusters and minimum entries per cluster for each participant group.

---

**Topic Representation**

Once clusters were established, topics were represented using a bag-of-words approach combined with **c-TF-IDF**. The vocabulary was controlled through `scikit-learn`’s `CountVectorizer` configured with a Portuguese stopword list, a minimum document frequency of 2 to exclude hapax terms, and an *n*-gram range of (1, 2) to allow multiword expressions to emerge.  

The resulting document-term matrix was then weighted with c-TF-IDF using **BM25**, which adjusts for frequency saturation and document length, thereby offering a more robust representation for small and unevenly sized clusters.

To enhance interpretability, several complementary strategies were then applied to generate alternative keyword sets. A **KeyBERT-inspired** re-ranking procedure adjusted weights by embedding similarity to the cluster centroid, ensuring semantic alignment. **Part-of-speech filtering** with `spaCy`’s Portuguese model (`pt_core_news_lg`) restricted descriptors to linguistically meaningful units such as noun phrases. To promote lexical diversity, **MMR** was applied to balance relevance and dissimilarity, reducing redundancy among terms.

Each of these methods produced an independent representation of the same topic, highlighting different facets of its content.

Finally, topic labels were generated using **GPT-4.1** through the OpenAI API. Each cluster was presented with its representative documents and keywords, and the model was prompted, in Portuguese, to produce a concise English label of at most 5 words. Although the input material was in Portuguese, English was chosen for consistency across groups and comparability with related work. The English translation of the prompt used for this step is shown below:

> ```
> I have a topic that contains the following set of documents: [DOCUMENTS]
> The topic is described by the following keywords: [KEYWORDS]
> Based on the above information, extract a short but highly descriptive topic label
> of no more than 5 words.
> Write it in English and make sure it is in the following format:
> topic: <topic label>
> ```

---

| **Method**       | **Representation Output**                                                                 |
|------------------|---------------------------------------------------------------------------------------------|
| c-TF-IDF         | `I can`, `to do`, `I started`, `time`, `things`, `honestly`, `girl`, `sleep`, `today`, `work` |
| KeyBERT          | `I feel`, `I do`, `too much`, `me`, `tired`, `time`, `myself`, `I see`, `currently`, `I want` |
| Part-of-speech    | `time`, `things`, `girl`, `interest`, `work`, `day`, `child`, `first`, `myself`, `special`   |
| MMR              | `to do`, `I started`, `time`, `things`, `sleep`, `I feel`, `I want`, `today`, `special interest` |
| GPT-4.1 Label     | `Student Life and Identity Struggles`                                                     |

#### Table 2. Different representations for a topic in the *Women with ADHD* group.

---

This multi-step process thus produced parallel perspectives on topic content:  
- **Statistical weighting** (c-TF-IDF)  
- **Semantic refinement** (KeyBERT)  
- **Linguistic filtering** (Part-of-speech)  
- **Diversity promotion** (MMR)  
- **Generative summarization** (GPT-4.1)  

**Table 2** illustrates these complementary outputs for a cluster in the *Women with ADHD* group. In particular, GPT-generated labels offered concise thematic summaries that proved particularly useful for comparing topics across groups, while the KeyBERT-derived keywords were retained for fine-grained analysis of cluster key terms in subsequent analyses.
