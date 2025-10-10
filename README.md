# Linguistic Patterns and Beliefs Related to ADHD in Adult Women: Creation and Analysis of a Portuguese Dataset <!-- omit from toc -->
This project is part of my Master's Thesis in Computer Science and Engineering, focusing on the creation and analysis of a Portuguese dataset to explore linguistic patterns and beliefs related to ADHD in adult women.

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)


# 📖 Table of Contents <!-- omit from toc -->

- [🎬 Introduction](#-introduction)
- [🎯 Research Questions](#-research-questions)
- [📊 Project Structure](#-project-structure)
- [💿 Datasets](#-datasets)
    - [📝 ADHD-Beliefs-PT Dataset](#-adhd-beliefs-pt-dataset)
    - [📝 ADHD Reddit Dataset](#-adhd-reddit-dataset)
- [💾 Installation](#-installation)
- [🖍️ Usage](#-usage)
- [📄 License](#-license)

## 🎬 Introduction

This research investigates linguistic patterns and beliefs related to ADHD in Portuguese-speaking adult women through computational analysis of the ADHD-Belliefs-PT dataset. The project combines natural language processing techniques with psychological insights to understand how ADHD experiences in this group are expressed linguistically.

## 🎯 Research Questions

- **RQ1**: Do Portuguese adult women with ADHD differ in linguistic style, lexical choice, or functional markers compared to other participants?
- **RQ2**: Do Portuguese adult women with ADHD write about different topics, themes, or experiences compared to other participants?

## 📊 Project Structure

```
📁 notebooks/adhd_beliefs_pt/
├── 01-data_preparation.ipynb               # Initial data setup and loading
├── 02-data_anonymization.ipynb             # Privacy protection measures
├── 03-data_visualizations.ipynb            # Exploratory data analysis
├── 04-data_preprocessing.ipynb             # Text cleaning and preparation
├── 05-rq1_liwc.ipynb                       # LIWC linguistic analysis
├── 06-rq1_* (binary comparisons)           # Statistical binary analyses
├── 07-rq1-group_comparison.ipynb           # (deprecated) Group comparison 
├── 08-generate_embeddings_serafim.ipynb    # Serafim Portuguese embeddings
├── 09-clustering.ipynb                     # Clustering analysis
├── 10-18 (topic modeling)                  # BERTopic and evaluation
```

## 💿 Datasets
This project utilizes two datasets:
1. **ADHD-Beliefs-PT**: A Portuguese dataset created for this research, containing text samples from 332 participants.
2. **Reddit ADHD Dataset**: An English dataset from Kaggle, used for initial testing and experimentation.

### 📝 ADHD-Beliefs-PT Dataset
The ADHD-Beliefs-PT dataset is a Portuguese dataset created for this research, containing text samples from 332 participants. The dataset includes demographic information and responses to open-ended questions about ADHD beliefs and experiences.
The dataset is not publicly available.


### 📝 ADHD Reddit Dataset
For the first tests and experimentation I'm utilizing the "Reddit ADHD Dataset" by user Jerseyneo on Kaggle. In the root directory of this project place the following commands in the terminal:

1. Downloading the dataset .zip via cURL
    ```bash
    #!/bin/bash
    curl -L -o ./data/datasets/reddit-adhd-dataset.zip\
        https://www.kaggle.com/api/v1/datasets/download/jerseyneo/reddit-adhd-dataset
    ```
2. Unzipping the dataset
    ```bash
    unzip ./data/datasets/reddit-adhd-dataset.zip -d ./data/datasets/reddit-adhd-dataset/
        rm ./data/datasets/reddit-adhd-dataset.zip
    ```


## 💾 Installation
This project uses **[uv](https://docs.astral.sh/uv/getting-started/installation/#installing-uv)** as the project manager of Python version and dependencies.

1. Install the required Python version for this project
    ```bash
    uv python install 3.13.0
    ```

2. Install Dependencies using uv
    ```bash
    uv sync
    ```
    This command will install all required dependencies for the project.

3. Install pre-commit hooks
    ```bash
    uv run pre-commit install
    ```

## 🖍️ Usage

### Running Notebooks

1. **Start Jupyter environment**
    ```bash
    uv run jupyter lab
    ```

2. **Execute notebooks in order** (01-18) for complete analysis pipeline

### Key Analysis Steps

- **Data Preparation**: Notebooks 01-04
- **Linguistic Analysis**: Notebooks 05-07  
- **Topic Modeling**: Notebooks 08-18

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.