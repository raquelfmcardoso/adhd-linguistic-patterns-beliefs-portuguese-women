The quality of a topic model cannot be judged by a single criterion. The clusters in an embedding space should be both internally consistent and distinct, while their keywords must yield coherent, interpretable topics. To capture these aspects, we employed two evaluation metrics—**Silhouette Coefficient** for internal cluster structure and **UMass Coherence** for external topic interpretability. These metrics are described in detail below.

---

**Silhouette Coefficient**

The **Silhouette Coefficient** measures how well a document fits its cluster by comparing its average distance to points within the cluster with its distance to the nearest other cluster, yielding a value between −1 and +1:

$$
s(i) = \frac{b(i) - a(i)}{\max\{a(i), b(i)\}}
$$

where $a(i)$ is the average distance between document *i* and all other points in its cluster, and $b(i)$ is the minimum average distance to points in any other cluster.  

Higher values indicate that documents fit well within their cluster and are distant from others, while values near 0 suggest overlap between clusters.

The coefficient was computed using `scikit-learn` in the **UMAP**-reduced embedding space used for clustering, excluding outliers flagged by **HDBSCAN** to avoid score distortion. Since HDBSCAN does not optimise for separation, the silhouette score provided an independent measure of cluster distinctiveness.  

In the context of **RQ2**, this metric ensures that the themes associated with women with and without ADHD are not simply artifacts of the algorithm but reflect genuinely distinct groupings in the underlying discourse.

---

**UMass Coherence**

While the silhouette score evaluates the geometric structure of clusters, coherence captures their interpretability. The **UMass Coherence** score measures how often the keywords defining a topic co-occur in the corpus. For a topic $T = \{w_1, \dots, w_M\}$, it is defined as:

$$
C_{UMass}(T) = \frac{2}{M(M-1)} \sum_{i=2}^{M} \sum_{j=1}^{i-1} \log \frac{ D(w_i, w_j) + \epsilon }{ D(w_j) }
$$

where $D(w_i, w_j)$ is the number of documents containing both words $w_i$ and $w_j$, $D(w_j)$ the document frequency of $w_j$, and $\epsilon = 1$ a smoothing constant to avoid division by zero.  

Higher values indicate greater coherence. Coherence was calculated over the top unigrams and bigrams from the `CountVectorizer`, excluding pairs absent from the vocabulary.

UMass coherence was chosen because it is **intrinsic**, relying only on the study corpus rather than external resources. This makes it well suited to European Portuguese, where such resources are scarce. It is also robust to smaller datasets of short, questionnaire-style responses, where external statistics can be noisy. Finally, its **negative-to-positive scale** enables direct comparison between groups.

---

Together, these measures provide complementary insights into model quality:  

- The **Silhouette Coefficient** assesses whether responses from each group form distinct and internally consistent clusters in embedding space.  
- The **UMass Coherence** evaluates whether the keywords describing those clusters represent meaningful linguistic patterns.  

In combination, they establish both the **structural validity** and the **semantic interpretability** of the topics, ensuring that subsequent group comparisons rest on a reliable modelling foundation.
