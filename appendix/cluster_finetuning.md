# Cluster Finetuning

The models selected for topic reduction are indicated in 🔵 **light blue**.

The final model configurations for each participant group are highlighted in 🟩 **light green**.

---

## Women with ADHD

### Clustering Results (different `minimum_topic_size`)

| **Metric \\ Min Size** | 🔵 **2** | **3** | **4** | **5** | **6** | **7** | **8** | **10** |
|--------------------------|------:|------:|------:|------:|------:|------:|------:|-------:|
| **Silhouette**           | 0.0491 | 0.0371 | 0.0464 | 0.0251 | 0.0600 | 0.0409 | 0.0567 | 0.0603 |
| **Average Coherence**    | -0.6998 | -1.1077 | -1.1033 | -1.0811 | -1.0777 | -1.2890 | -1.1353 | -1.1598 |
| **Outliers**             | 6 | 7 | 6 | 3 | 24 | 25 | 20 | 30 |
| **Topics**               | 9 | 5 | 5 | 2 | 4 | 3 | 3 | 2 |

*Table: Women with ADHD clustering results with different `minimum_topic_size`.*

---

### Reduced Topics (different topic numbers)

| **Metric \\ Clusters** | **2** | **3** | **4** | **5** | **6** | **7** | 🟩 **8** |
|--------------------------|------:|------:|------:|------:|------:|------:|------:|
| **Silhouette**           | 0.0737 | 0.0606 | 0.0489 | 0.0274 | 0.0445 | 0.0458 | **0.0523** |
| **Average Coherence**    | -0.4874 | -0.6641 | -0.6600 | -0.6874 | -0.8182 | -0.7591 | **-0.7402** |

*Table: Women with ADHD `reduce_topics` results with different topic numbers.*

---

## Women without ADHD

### Clustering Results (different `minimum_topic_size`)

| **Metric \\ Min Size** | **2** | 🔵 **3** | **4** | **5** | **6** | **7** | **8** | **10** |
|--------------------------|------:|------:|------:|------:|------:|------:|------:|-------:|
| **Silhouette**           | 0.0365 | 0.0419 | 0.0464 | 0.0291 | 0.0371 | 0.0396 | 0.0471 | 0.0449 |
| **Average Coherence**    | -0.9958 | -1.1011 | -1.3479 | -1.3794 | -1.3923 | -1.3058 | -1.3482 | -1.3321 |
| **Outliers**             | 27 | 37 | 24 | 36 | 40 | 65 | 68 | 69 |
| **Topics**               | 35 | 23 | 12 | 12 | 9 | 7 | 7 | 4 |

*Table: Women without ADHD clustering results with different `minimum_topic_size`.*

---

### Reduced Topics (different topic numbers)

| **Metric \\ Clusters** | **10** | **13** | **14** | 🟩 **15** | **16** | **17** |
|--------------------------|------:|------:|------:|------:|------:|------:|
| **Silhouette**           | 0.0345 | 0.0427 | 0.0405 | **0.0439** | 0.0371 | 0.0354 |
| **Average Coherence**    | -1.1133 | -1.1486 | -1.1245 | **-1.1313** | -1.1012 | -1.1348 |

*Table: Women without ADHD `reduce_topics` results.*

---

## Participants with ADHD

### Clustering Results (different `minimum_topic_size`)

| **Metric \\ Min Size** | 🟩 **2** | **3** | **4** | **5** | **6** | **7** | **8** | **10** |
|--------------------------|------:|------:|------:|------:|------:|------:|------:|-------:|
| **Silhouette**           | **0.0434** | 0.0522 | 0.0261 | 0.0261 | 0.0261 | 0.0261 | 0.0261 | 0.0305 |
| **Average Coherence**    | **-0.9028** | -1.0506 | -1.0631 | -1.0631 | -1.0631 | -1.0631 | -1.0631 | -1.0649 |
| **Outliers**             | **11** | 11 | 0 | 0 | 0 | 0 | 0 | 9 |
| **Topics**               | **13** | 7 | 3 | 3 | 3 | 3 | 3 | 2 |

*Table: Participants with ADHD clustering results with different `minimum_topic_size`.*

---

## Participants without ADHD

### Clustering Results (different `minimum_topic_size`)

| **Metric \\ Min Size** | **2** | 🔵 **3** | **4** | **5** | **6** | **7** | **8** | **10** |
|--------------------------|------:|------:|------:|------:|------:|------:|------:|-------:|
| **Silhouette**           | 0.0421 | 0.0539 | 0.0464 | 0.0456 | 0.0428 | 0.0362 | 0.0366 | 0.0366 |
| **Average Coherence**    | -1.0519 | -1.1910 | -1.3236 | -1.3693 | -1.5301 | -1.4909 | -1.4421 | -1.4421 |
| **Outliers**             | 43 | 48 | 50 | 67 | 92 | 7 | 9 | 8 |
| **Topics**               | 59 | 36 | 27 | 20 | 15 | 4 | 4 | 4 |

*Table: Participants without ADHD clustering results with different `minimum_topic_size`.*

---

### Reduced Topics (different topic numbers)

| **Metric \\ Clusters** | **21** | **23** | **25** | 🟩 **26** | **27** | **30** | **32** |
|--------------------------|------:|------:|------:|------:|------:|------:|------:|
| **Silhouette**           | 0.0470 | 0.0537 | 0.0542 | **0.0559** | 0.0554 | 0.0553 | 0.0495 |
| **Average Coherence**    | -1.2570 | -1.2516 | -1.1965 | **-1.1804** | -1.1965 | -1.2019 | -1.1857 |

*Table: Participants without ADHD `reduce_topics` results with different topic numbers.*
