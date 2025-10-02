# Data Curation

This section describes our **curation pipeline** and the **ablation experiment** conducted to measure its effectiveness.

---

## Folder Structure

```
iclr-submission/
 ├── data_curation/
 │    ├── curation/
 │    │    ├── cc_curator.py
 │    │    ├── language_detector.py
 │    │    ├── nemo_curator.py
 │    │    ├── streaming_regex.py
 │    ├── deduplication/
 │    │    ├── deduplication.py
 │    │    └── deduplication.sh
 │    ├── toxic_filter/
 │    │    ├── sample_toxic_words.txt
 │    │    ├── toxic_filter_inference.py
 │    │    └── toxic_filter_rule.py
 │    ├── quality_filter/
 │    │    ├── quality_filter.py
 │    └── README.md
```
---

## Curation Pipeline Overview

**Pipeline Diagram**
![Curation Pipeline](/readme-resources/data-curation.png)

**Description of Stages**

1. **Raw Corpus Construction**

   * Aggregate large-scale text from publicly available sources (English + Hindi).
2. **Deduplication and Cleaning**

   * NeMo Curator deduplication (DCLM)
   * Filter by word/character distribution statistics (FWE filtering)
3. **Quality Filtering**

   * Document-level filtering: removal of boilerplate, low-information pages, and noise
   * Language ID filtering (restricting to English + Hindi)
4. **Indian Language Adaptation**

   * Language-specific tokenization and normalization for Hindi
   * Script unification for consistent Unicode handling
5. **Final Curated Dataset**

   * High-quality, domain-diverse corpus passed to training

---

## Evaluation Procedure

To rigorously assess the impact of our **curation pipeline**, we conducted a controlled evaluation comparing models trained on **conventional datasets** versus **curated datasets**.

**Purpose:**
The evaluation aims to quantify the benefit of data curation on model performance across multiple reasoning and knowledge benchmarks, isolating the effect of data quality from scale.

**Benchmarks Used:**
We selected widely recognized benchmarks to capture diverse aspects of LLM capabilities:

* **[ARC Challenge & ARC Easy](https://huggingface.co/datasets/allenai/ai2_arc)** – reasoning-focused multiple-choice questions. 
* **[HellaSwag (English & Hindi)](https://huggingface.co/datasets/Rowan/hellaswag)** – commonsense reasoning and next-event prediction.
* **[MMLU (English & Hindi)](https://huggingface.co/datasets/cais/mmlu)** – multitask knowledge evaluation across academic and professional subjects.

**Evaluation Strategy:**

* For this experiment, we selected the [Param-1](https://huggingface.co/bharatgenai/Param-1) pre-trained checkpoint, trained on 5T tokens, as our baseline due to its bilingual capabilities, making it well-suited for our evaluation. We then performed extended continual pretraining on this model using 2T tokens, drawn from the DCLM corpus, with 30% of the data translated into Hindi, under both conventional and curated data conditions.
* Both datasets were **matched in size (2T tokens)** to ensure that performance differences reflect the effect of curation rather than data volume.
* Performance was evaluated using standard benchmark metrics to measure gains in reasoning, multilingual understanding, and robustness.

**Key Expectations:**
We anticipate that models trained on curated datasets will demonstrate:

1. Higher accuracy across all benchmarks.
2. Improved performance on **low-resource and multilingual settings** (e.g., Hindi variants).
3. Reduced propagation of low-quality, toxic, or redundant content, contributing to safer and more reliable outputs.

This evaluation framework establishes a **clear, reproducible methodology** for testing the efficacy of data curation, providing actionable insights for both ongoing model development and future dataset construction.

---

### Ablation Experiment 1: Evaluating the Efficacy of the Curation Pipeline

For this ablation study, we selected a **pre-trained checkpoint of an open-source LLM, [Param-1](https://huggingface.co/bharatgenai/Param-1)**, a **2.9B-parameter bilingual model** supporting English and Hindi. This checkpoint was trained on **5T tokens**, providing a strong multilingual baseline for our evaluation.

> *Based on our internal experimentation, we empirically observe scaling effects consistent across small, medium, and large model regimes*
> [Scaling Laws for Neural Language Models](https://ar5iv.labs.arxiv.org/html/2001.08361),
> [Unraveling the Mystery of Scaling Laws: Part I](https://arxiv.org/abs/2403.06563),
> [Scaling Law for Language Models Training Considering Batch Size](https://arxiv.org/html/2412.01505),
> [Language models scale reliably with over-training and on downstream tasks](https://www.emergentmind.com/papers/2403.08540)

**Model Details:**

* **Model:** Param-1 Pre-trained Checkpoint (2.9B parameters)
* **Checkpoint Source:** [Hugging Face: Param-1 PT1](https://huggingface.co/bharatgenai/Param-1)
* **Training Recipe:** As described in the [Param Paper](https://arxiv.org/pdf/2507.13390)
* **Pretraining Tokens:** Original pretraining: 5T tokens; extended continual pretraining for ablation: 2T tokens

## Training Data Composition

To systematically evaluate the effect of data curation, we conducted **extended continual pretraining** on 2T tokens under **two controlled conditions**:

1. **Conventional Corpus (Uncurated)**

   * Constructed directly from raw text with minimal preprocessing (tokenization, basic normalization).
   * The 2T-token subset was sampled from the [DCLM corpus](https://github.com/mlfoundations/dclm), with **30% of tokens translated into Hindi** to maintain bilingual coverage.
   * No additional quality filters were applied, ensuring a baseline reflecting typical large-scale pretraining data.

2. **Curated Corpus (Curation Applied)**

   * Derived from the same underlying sources as the conventional corpus.
   * Processed through the **NeMo Curator pipeline**, which applies multiple quality control steps:

     * Deduplication
     * Heuristic-based filtering
     * PII redaction
     * Toxicity filtering
     * Quality scoring (low, medium, high)
   * A fully curated **2T-token subset** was selected, strictly matching the conventional corpus in size to isolate the effect of curation.

**Key Design Considerations:**

* Both datasets contain **exactly 2T tokens**, eliminating confounding effects of scale.
* By maintaining identical token counts, any observed performance differences can be confidently attributed to **data quality and curation**.
* Inclusion of **30% Hindi tokens** ensures that the evaluation captures bilingual performance, addressing potential reviewer concerns regarding language coverage.

---

## Experiment Replication Procedure

The complete set of scripts and codebase required to replicate this experiment will be provided below.

## Curation Scripts and Codebase

All scripts are provided under [`iclr-submission/Data_Curation/`](experiments/data_curation/).

## Key Components

* `curation/curator.py` → Curation Pipeline (Cleaning, Heuristic Filters, Redact PII etc.)
* `deduplication/deduplciation.sh` → Bash file for global deduplication
* `quality_filter/quality_filter.py` → Quality Filter (Low, Medium, High)
* `toxic_filter/toxic_filter_rule.py` → Rule Based Toxic Filtering (word list included for 1 language)

---

## Steps to Run

1. **Setup Environment**

   ```bash
   conda create -n curator python=3.10 -y
   conda activate curator
   pip install nemo_toolkit[all] transformers datasets
   ```

2. **Download Raw Corpus**

   ```bash
   bash scripts/download_raw.sh --languages en,hi --output data/raw/
   ```

3. **Run Curation Pipeline**

   ```bash
   bash scripts/run_curator.sh --config configs/curator.yaml \
                               --input data/raw/ \
                               --output data/curated/
   ```

4. **Inspect Curated Data**

   ```bash
   jupyter notebook notebooks/quality_checks.ipynb
   ```

5. **Use in Pretraining**

   * Curated and non-curated corpora are directly pluggable into the NeMo pretraining recipes.
   * Training scripts are provided under [`experiments/pretraining/`](experiments/pretraining/).

---

### Results Obtained: Conventional vs Curated

## Evaluation Procedure
We evaluated models trained on both conventional datasets (raw corpus with minimal preprocessing) and curated datasets (data refined with targeted filtering and quality improvements). The goal was to compare their performance across widely used benchmarks for LLM evaluation.

## Conventional vs Curated Data Sample

![Curation Sample](/readme-resources/curation.png)

### Benchmark Table
| **Model**      | **ARC Challenge** | **ARC Easy** | **Hella Swag** | **Hella Swag Hi** | **MMLU** | **MMLU Hi** |
|----------------|------------------:|--------------:|----------------:|------------------:|---------:|------------:|
| Conventional   | 46.5              | 73.6          | 73.5            | 28.9              | 41.3     | 26.2        |
| Curated        | 53.6              | 74.2          | 73.8            | 41.4              | 46.2     | 34.6        |

### Ablation Experiment 2: Toxicity Comparison

![Toxicity Sample](/readme-resources/toxic-comparison)

### Observation of the Resutls

We observe that after performing curation increase in the score on the various benhcmarks are obtained.
