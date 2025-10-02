---

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
Here’s a polished and professional **“Evaluation Overview”** section you can put in your GitHub repo, right before the experiment details:

---

## Evaluation Overview

To rigorously assess the impact of our **curation pipeline**, we conducted a controlled evaluation comparing models trained on **conventional datasets** versus **curated datasets**.

**Purpose:**
The evaluation aims to quantify the benefit of data curation on model performance across multiple reasoning and knowledge benchmarks, isolating the effect of data quality from scale.

**Benchmarks Used:**
We selected widely recognized benchmarks to capture diverse aspects of LLM capabilities:

* **[ARC Challenge & ARC Easy](https://huggingface.co/datasets/allenai/ai2_arc)** – reasoning-focused multiple-choice questions. 
* **[HellaSwag (English & Hindi)](https://huggingface.co/datasets/Rowan/hellaswag)** – commonsense reasoning and next-event prediction.
* **[MMLU (English & Hindi)](https://huggingface.co/datasets/cais/mmlu)** – multitask knowledge evaluation across academic and professional subjects.

**Evaluation Strategy:**

* Models were trained using a **pre-trained 2.9B parameter checkpoint (Param-1 PT1)**, with extended continual pretraining on 2T tokens under both conventional and curated data conditions.
* Both datasets were **matched in size (2T tokens)** to ensure that performance differences reflect the effect of curation rather than data volume.
* Performance was evaluated using standard benchmark metrics to measure gains in reasoning, multilingual understanding, and robustness.

**Key Expectations:**
We anticipate that models trained on curated datasets will demonstrate:

1. Higher accuracy across all benchmarks.
2. Improved performance on **low-resource and multilingual settings** (e.g., Hindi variants).
3. Reduced propagation of low-quality, toxic, or redundant content, contributing to safer and more reliable outputs.

This evaluation framework establishes a **clear, reproducible methodology** for testing the efficacy of data curation, providing actionable insights for both ongoing model development and future dataset construction.

---

### Ablation Experiment 1: To Check the efficacy of the Curation Pipeline. 

For Ablation study purposes we chose the a pre-trained checkpoint of an open source LLM, [Param-1 PT1](https://huggingface.co/bharatgenai/Param-1) which is a 2.9B parameter range-bilingual model. 

_Based on our internal experimentation, we have empirically observed a scaling effect applicable from small models to typical medium sized and large size models._
https://ar5iv.labs.arxiv.org/html/2001.08361
https://arxiv.org/abs/2403.06563
https://arxiv.org/html/2412.01505
https://www.emergentmind.com/papers/2403.08540

* **Model**: Param-1 Pre-Trained Ckpt (2.9B parameters)
* **Checkpoint Source**: [Hugging Face: Param-1 PT1](https://huggingface.co/bharatgenai/Param-1)
* **Training Recipe**: As described in [Param Paper](https://arxiv.org/pdf/2507.13390)
* **Tokens Trained**: This model is a pretrained checkpoint with 5T tokens, and we perform extended continual pretraining on it with 2T tokens for ablation study.

---

## Training Data Composition

For the extended training phase, we utilized **2T tokens** under two distinct conditions to enable a controlled comparison:

1. **Conventional Corpus (Without Curation)**

   * Constructed directly from raw text with only minimal preprocessing applied.
   * The 2T-token subset was sampled from the [DCLM](https://github.com/mlfoundations/dclm) corpus.

2. **Curated Corpus (With Curation)**

   * Derived from the same underlying sources as the conventional corpus, but processed through the **NeMo Curator pipeline** for quality filtering and curation.
   * A 2T-token subset was selected to match the conventional corpus in size.

Both datasets contain **exactly 2T tokens**, ensuring that any observed differences in model performance can be attributed to the effect of curation rather than scale.

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
