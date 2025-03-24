# Linguistic Patterns and Beliefs Related to ADHD in Adult Women: Creation and Analysis of a Portuguese Dataset <!-- omit from toc -->
This project is part of my Master's Thesis in Computer Science and Engineering, focusing on the creation and analysis of a Portuguese dataset to explore linguistic patterns and beliefs related to ADHD in adult women.

# 📖 Table of Contents <!-- omit from toc -->

- [🎬 Introduction](#-introduction)
- [💿 Datasets](#-datasets)
    - [📝 ADHD Reddit Dataset](#-adhd-reddit-dataset)
- [💾 Installation](#-installation)
- [🖍️ Usage](#-usage)

## 🎬 Introduction
<!-- Add a brief introduction about the project and its objectives. -->


## 💿 Datasets
For the first tests and experimentation I'm utilizing the "Reddit ADHD Dataset" by user Jerseyneo on Kaggle.

### 📝 ADHD Reddit Dataset
In the root directory of this project place the following commands in the terminal:

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
<!-- Explain how to use the project, including examples if necessary. -->

