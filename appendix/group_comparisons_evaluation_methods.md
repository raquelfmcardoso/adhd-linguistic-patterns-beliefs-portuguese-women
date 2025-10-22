To fully address **RQ2**, it was necessary not only to evaluate the internal quality and interpretability of the topic models, but also to compare topic distributions across groups. For this purpose, we applied both **similarity analysis** and statistical testing using **Fisher’s Exact Test**, **Jensen–Shannon Divergence (JSD)**, and a **permutation test**. These methods are described below.

---

**Similarity Analysis**

Comparing independently trained topic models requires principled topic alignment, as models may yield different numbers of clusters and labels.  
We implemented a **similarity-based procedure**:

1. For each model, the top thirty keywords with weights were extracted to form **topic–word weight matrices**.  
2. A shared vocabulary was constructed, and each topic represented as a **normalized vector** in this space.  
3. Pairwise **cosine similarity** between all topics produced an $ n \times m $ similarity matrix.  
4. **Optimal one-to-one correspondences** were identified using the *Linear Sum Assignment* algorithm from `scipy`, which maximizes overall similarity.

Similarity thresholds $\tau \in \{0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40\}$ were then applied: topics above the threshold were considered **aligned**, while those below were treated as **group-specific**. This process produced aligned document count vectors for subsequent statistical testing.

Thresholds were chosen to balance four goals:
- Maximizing effect size  
- Ensuring statistical significance  
- Maintaining high similarity  
- Enhancing meaningful correspondences  

To account for sampling variability in topic distributions, **bootstrap confidence intervals (CIs)** were computed for JSD estimates.  
Document-topic assignments were resampled with replacement 1000 times within each group, and divergence recalculated for each resample. This provided robust uncertainty estimates, isolating sampling variability from alignment variability.

---

**Fisher’s Exact Test**

To assess whether **ADHD status** was associated with differences in topic allocation, we used an **exact test of independence**.  
After alignment, each comparison was represented as a $ 2 \times 2 $ contingency table contrasting documents assigned to **group-specific topics** with those assigned to **shared topics**, where $a$ and $b$ are counts for one group and $c$ and $d$ are counts for the other. In this setup, $a$ and $c$ correspond to group-specific topics.

The probability of observing the model’s configuration under the null hypothesis follows the **hypergeometric distribution**:

$$
p = \frac{\binom{a+b}{a}\binom{c+d}{c}}{\binom{n}{a+c}}, \quad n = a + b + c + d
$$

The null hypothesis ($ H_0 $) states that ADHD status has **no effect** on whether participants wrote about shared or group-specific themes.  
This exact test is appropriate because some clusters contain few documents, making asymptotic approaches such as $ \chi^2 $ unreliable.  

Implementation with `scipy` yielded both an **odds ratio** and a **two-tailed exact p-value**:
- Odds ratio $ > 1 $: greater likelihood of group-specific topic usage  
- Odds ratio $ < 1 $: preference for shared topics  

Results were interpreted using the conventional threshold of $ p \leq 0.05 $, providing a direct test of dependency between ADHD status and linguistic organizational strategies.

---

**Jensen–Shannon Divergence (JSD)**

While Fisher’s test establishes **statistical significance**, it does not capture **magnitude**. As a proxy for effect size, we computed the **Jensen–Shannon Divergence (JSD)** between group-level topic distributions.  
Although its scale differs from conventional effect size measures, JSD provides a useful approximation of distributional differences.

The related **Kullback–Leibler (KL) divergence** is defined as:

$$
KL(P \,\|\, Q) = \sum_i P(i) \log \frac{P(i)}{Q(i)}
$$

and measures the information cost of using one group’s topic distribution to approximate another’s.  
The **JSD** extends this by symmetrizing the comparison and ensuring finiteness:

$$
JSD(P \,\|\, Q) = \tfrac{1}{2} KL(P \,\|\, M) + \tfrac{1}{2} KL(Q \,\|\, M), \quad M = \tfrac{1}{2}(P + Q)
$$

Here, $ P $ and $ Q $ are group-level topic distributions, and $ M $ their midpoint. Conceptually, JSD reflects the **extra information** needed to describe one group’s thematic structure using the other’s as a baseline.  

We used the `scipy` implementation for JSD, which returns $ \sqrt{JSD(P \,\|\, Q)} $, bounded between 0 (identical) and 1 (disjoint). Using base 2 expresses the divergence in bits and normalizes the maximum to 1.

For interpretation:  
- **< 0.1** → negligible difference  
- **0.1–0.3** → small to moderate difference  
- **0.3–0.5** → large difference  
- **> 0.5** → very large difference  

Within the scope of RQ2, JSD quantifies how differently women with ADHD and comparison groups distribute attention across topics, providing an interpretable measure of **thematic divergence**.

---

**Permutation Test**

To assess whether observed divergences could plausibly arise by chance, we implemented a **Non-Parametric Permutation Test**.  
This analysis tests the null hypothesis that participants from the groups being compared have **identical topic usage patterns**.

The procedure involved:
1. Creating a **combined BERTopic model** trained on all responses from both groups, ensuring both were represented in the same topic space.  
2. Calculating the observed JSD between the topic distributions of the two groups within this shared space.  
3. Randomly shuffling group labels **1000 times** while preserving group sizes and topic assignments, recalculating JSD for each shuffled configuration to generate a null distribution.

The **permutation p-value** was defined as the proportion of shuffled configurations producing JSD values greater than or equal to the observed value.  
Following convention:
- $ p < 0.05 $: statistically significant  
- $ p = 0.0 $: reported as $ p < 0.001 $, reflecting the resolution limit of $ 1 / n_{\text{permutations}} $

This approach provides an **assumption-free test** of whether topic distribution differences represent genuine group characteristics or could reasonably be explained by sampling variability alone.
