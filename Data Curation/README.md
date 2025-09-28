Data Curation

Curation Pipeline overiview:
Diagram comes here

Explanation of the curation steps

PT Chckpt link from teh Param 1 PT hugging face

Training Data COmposition: 
1. W/o curated: link to download 
2. w curated: link to download

Curation Scripts and code bases
Steps to run the code base


---

# Data Curation

This section describes our **curation pipeline** and the **ablation experiment** conducted to measure its effectiveness.

---

## Curation Pipeline Overview

**Pipeline Diagram**
*(Figure will be inserted here in the final camera-ready — e.g., an end-to-end curation workflow illustration)*

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

## Base Pretraining Checkpoint

For Ablation study purposes we chose the 2.9B param range of model to test it on.
Based on our internal experimentatin , we have empirically observed a scaling effect applicable from small models to typical medium sized and large size models.
https://ar5iv.labs.arxiv.org/html/2001.08361
https://arxiv.org/abs/2403.06563
https://arxiv.org/html/2412.01505
https://www.emergentmind.com/papers/2403.08540

* **Model**: Param-1 PT (2.9B parameters)
* **Checkpoint Source**: [Hugging Face: Param-1 PT1](https://huggingface.co/bharatgenai/Param-1)
* **Training Recipe**: As described in [Param Paper](https://arxiv.org/pdf/2507.13390)
* **Tokens Trained**: 5T (before this ablation experiment)

---

## Training Data Composition

We extended training with **2T tokens** under two conditions:

1. **Without Curation** (Conventional Corpus)

   * Raw text with only basic preprocessing
   * Download: `https://example.com/datasets/param_ablation/english_hindi_noncurated`

2. **With Curation** (Curated Corpus via Pipeline)

   * Same sources passed through the NeMo Curator pipeline
   * Download: `https://example.com/datasets/param_ablation/english_hindi_curated`

Both datasets are matched in size (**2T tokens**) to ensure comparability.

---

## Curation Scripts and Codebase

All scripts are provided under [`experiments/data_curation/`](experiments/data_curation/).

### Key Components

* `configs/curator.yaml` → Pipeline configuration file (deduplication, filtering thresholds, LID models, etc.)
* `scripts/run_curator.sh` → End-to-end script to process raw corpus into curated corpus
* `scripts/download_raw.sh` → Helper script to fetch raw corpus shards (English + Hindi)
* `notebooks/quality_checks.ipynb` → Post-curation quality analysis notebook

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

## Folder Structure

```
experiments/
 ├── data_curation/
 │    ├── configs/
 │    │    └── curator.yaml
 │    ├── scripts/
 │    │    ├── run_curator.sh
 │    │    ├── download_raw.sh
 │    ├── notebooks/
 │    │    └── quality_checks.ipynb
 │    └── README.md
 ├── pretraining/
 │    ├── train_curated.sh
 │    ├── train_noncurated.sh
 │    └── configs/
 │         └── param_ablation.yaml
```

---

This makes it look **professional, technical, and reproducible**. It has:

* **Pipeline overview + explanation**
* **Exact PT checkpoint link**
* **Data composition with download links (placeholders now, can be replaced)**
* **Scripts + step-by-step usage**
* **Standard folder structure**

---


### Results Obtained

### Benchmark Results: Conventional vs Curated

| **Model**      | **ARC Challenge** | **ARC Easy** | **Hella Swag** | **Hella Swag Hi** | **MMLU** | **MMLU Hi** |
|----------------|------------------:|--------------:|----------------:|------------------:|---------:|------------:|
| Conventional   | 46.5              | 73.6          | 73.5            | 28.9              | 41.3     | 26.2        |
| Curated        | 53.6              | 74.2          | 73.8            | 41.4              | 46.2     | 34.6        |


### Observation of the Resutls

We observe that after performing curation increase in the score on the various benhcmarks are obtained.
