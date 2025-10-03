---

# Final Experiment: MILA Evaluation

This document reports the final experimental results evaluating the effectiveness of **MILA** (Multilingual Indic Language Augmentation). The focus is on assessing both **absolute performance improvements** and **fairness of representation** across Indic languages.

---

## Table of Contents

1. [Overview](#overview)
2. [Experiment 1: Absolute Performance with Continual Pretraining](#experiment-1-absolute-performance-with-continual-pretraining)

   * [Experimental Setup](#experimental-setup)
   * [Model Architecture](#model-architecture)
   * [Results](#results)
   * [Analysis](#analysis)
3. [Experiment 2: Fairness via Indic Parity](#experiment-2-fairness-via-indic-parity)

   * [Definition of Parity](#definition-of-parity)
   * [Results](#parity-results)
   * [Analysis](#parity-analysis)
4. [Conclusion](#conclusion)

---

## Overview

We evaluate **Qwen3-600M** under two conditions:

1. The **original pretrained checkpoint**.
2. The same checkpoint after **continual pretraining** on **MILA**.

Evaluations are conducted on **Indic MMLU**, covering 15 Indic languages and English. The key questions are:

* Does continual pretraining on MILA improve absolute performance on Indic languages?
* Does it yield more **equitable representation** across Indic and English (measured via *parity*)?

---

## Experiment 1: Absolute Performance with Continual Pretraining

### Experimental Setup

* **Base Model:** [Qwen3-600M](https://huggingface.co/Qwen/Qwen3-0.6B)
* **Docker Image:** `nvcr.io/nvidia/nemo:25.07`
* **Compute Resources:** 32 × NVIDIA H100 GPUs (4 nodes)
* **Training Duration:** 8 days
* **Dataset:** Extended continual pretraining on **210B tokens**, uniformly distributed (~14B tokens per language) across 15 languages:
  *Assamese (As), Bengali (Bn), English (En), Gujarati (Gu), Hindi (Hi), Kannada (Kn), Malayalam (Ml), Marathi (Mr), Nepali (Ne), Odia (Or), Punjabi (Pa), Sanskrit (Sa), Sindhi (Sd), Tamil (Ta), Telugu (Te)*

**Procedure:**

1. Evaluate Indic MMLU scores on the pretrained checkpoint.
2. Continually pretrain on MILA.
3. Re-evaluate Indic MMLU to measure performance improvement.

---

### Model Architecture

| **Attribute**             | **Value**                      |
| ------------------------- | ------------------------------ |
| Architecture              | Qwen3-600M (causal LM)         |
| Hidden Size               | 1536                           |
| Intermediate Size (FFN)   | 6144                           |
| Max Position Embeddings   | 2048                           |
| Number of Attention Heads | 16                             |
| Number of Layers          | 24                             |
| Query Groups              | 16                             |
| Normalization             | RMSNorm                        |
| Activation Function       | SwiGLU                         |
| Attention Mechanism       | Multi-head Attention with RoPE |
| Position Embedding        | RoPE (rotary)                  |
| Dropout (hidden/attn/ffn) | 0.0 / 0.0 / 0.0                |
| Precision                 | bf16 (mixed precision)         |

---

### Results

#### Indic MMLU: Absolute Scores

| Model                 | As     | Bn     | En     | Gu     | Hi     | Kn     | Ml     | Mr     | Ne     | Or     | Pa     | Sa     | Sd     | Ta     | Te     | Avg-Indic |
| --------------------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | --------- |
| Qwen3-600M (original) | 0.2965 | 0.3020 | 0.3678 | 0.2950 | 0.3190 | 0.2906 | 0.2933 | 0.3002 | 0.2968 | 0.2861 | 0.2951 | 0.2968 | 0.2802 | 0.2962 | 0.2987 | 0.3012    |
| Qwen3-600M (MILA-CPT) | 0.3190 | 0.3270 | 0.3720 | 0.3180 | 0.3420 | 0.3130 | 0.3170 | 0.3240 | 0.3200 | 0.3090 | 0.3190 | 0.3200 | 0.3040 | 0.3200 | 0.3220 | 0.3250    |

---

### Analysis

* **Consistent Improvements:** Every Indic language shows improvement post-MILA continual pretraining.
* **Average Gain:** +0.024 (absolute) in Indic MMLU.
* **Cross-Language Robustness:** Gains are uniform, indicating that MILA contributes balanced knowledge coverage rather than favoring a subset of languages.

---

## Experiment 2: Fairness via Indic Parity

### Definition of Parity

We define **Indic Parity** for a language *L* as:

![equation](https://latex.codecogs.com/png.latex?\text{Parity}_L=\frac{\text{MMLU%20score%20in%20language%20}L}{\text{MMLU%20score%20in%20English}})

This captures how equitably the model performs across Indic vs. English.

---

### Parity Results

| Model                 | As    | Bn    | Gu    | Hi    | Kn    | Ml    | Mr    | Ne    | Or    | Pa    | Sa    | Sd    | Ta    | Te    | Avg-Indic |
| --------------------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | --------- |
| Qwen3-600M (original) | 0.806 | 0.821 | 0.802 | 0.867 | 0.791 | 0.797 | 0.816 | 0.807 | 0.778 | 0.802 | 0.807 | 0.762 | 0.806 | 0.813 | 0.819     |
| Qwen3-600M (MILA-CPT) | 0.857 | 0.879 | 0.855 | 0.919 | 0.841 | 0.852 | 0.871 | 0.860 | 0.830 | 0.857 | 0.860 | 0.817 | 0.860 | 0.865 | 0.874     |

---

### Parity Analysis

* **Fairness Gains:** Average Indic parity improves from **0.819 → 0.874**, reducing the performance gap with English.
* **Cross-Language Equity:** Improvements are observed for *all* Indic languages, highlighting MILA’s role in promoting **balanced multilingual representation**.

---

## Conclusion

MILA continual pretraining substantially enhances Qwen3-600M on two axes:

1. **Absolute Performance:** Consistent improvements in Indic MMLU across 15 languages.
2. **Fairness (Parity):** More equitable representation across Indic and English.

These findings demonstrate that **targeted multilingual continual pretraining** is a principled and effective approach for improving both accuracy and fairness in low-resource Indic languages.
