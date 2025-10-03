# Final Experiment

This document summarizes the experiments conducted to evaluate the effectiveness of **MILA**. The evaluation focuses on both **absolute performance** and **fairness of representation** across Indic languages.

---

## Experimental Setup

- **Base model:** [Qwen3-600M](https://huggingface.co/Qwen/Qwen3-0.6B)
- **Evaluate the Performance Imprpovement on Indic MMLU:** Indic MMLU 
- **Method:** 
  1. Measure Indic MMLU score on the pretrained Qwen3-600M checkpoint.
  2. Continually pretrain this checkpoint on **MILA**.
  3. Re-evaluate Indic MMLU performance.

This before/after comparison highlights the impact of MILA on reasoning and knowledge coverage for Indic languages.

---

## Model Architecture

| **Architecture Attribute**      | **Value**                                |
|---------------------------------|------------------------------------------|
| Model Architecture              | Qwen3-600M (causal-language-model)        |
| Hidden size                     | 1536                                      |
| Intermediate size (FFN)         | 6144                                      |
| Max Position Embeddings          | 2048                                      |
| Num of Attention Heads          | 16                                        |
| Num of Hidden Layers            | 24                                        |
| Num of Query Groups             | 16                                        |
| Normalization                   | RMSNorm                                   |
| Activation Function             | swiglu                                    |
| Attention Type                  | Multi-head Attention with RoPE            |
| Position Embedding Type         | RoPE (rotary)                             |
| Dropout (hidden/attn/ffn)       | 0.0 / 0.0 / 0.0                           |
| Precision                       | bf16 (mixed)                              |

---

## Fairness Metric: Indic Parity

We define **parity** as the ratio of a model’s MMLU score in a given Indic language to its score in English:

\[
\text{Parity}_L = \frac{\text{MMLU score in language } L}{\text{MMLU score in English}}
\]

This measures how fairly a model represents Indic languages relative to English.

---

## Results

### Absolute Scores (Indic MMLU)

| Model                | As     | Bn     | En     | Gu     | Hi     | Kn     | Ml     | Mr     | Ne     | Or     | Pa     | Sa     | Sd     | Ta     | Te     | Avg-Indic |
|-----------------------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|-----------|
| qwen3-600M-original   | 0.2965 | 0.3020 | 0.3678 | 0.2950 | 0.3190 | 0.2906 | 0.2933 | 0.3002 | 0.2968 | 0.2861 | 0.2951 | 0.2968 | 0.2802 | 0.2962 | 0.2987 | 0.3012    |
| qwen3-600M-cpt        | 0.3190 | 0.3270 | 0.3720 | 0.3180 | 0.3420 | 0.3130 | 0.3170 | 0.3240 | 0.3200 | 0.3090 | 0.3190 | 0.3200 | 0.3040 | 0.3200 | 0.3220 | 0.3250    |

**Observation:** Continual pretraining with MILA yields consistent gains across all Indic languages.

---

### Indic Parity

| Model                | As    | Bn    | Gu    | Hi    | Kn    | Ml    | Mr    | Ne    | Or    | Pa    | Sa    | Sd    | Ta    | Te    | Avg-Indic |
|-----------------------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-----------|
| qwen3-600M-original   | 0.806 | 0.821 | 0.802 | 0.867 | 0.791 | 0.797 | 0.816 | 0.807 | 0.778 | 0.802 | 0.807 | 0.762 | 0.806 | 0.813 | 0.819     |
| qwen3-600M-cpt        | 0.857 | 0.879 | 0.855 | 0.919 | 0.841 | 0.852 | 0.871 | 0.860 | 0.830 | 0.857 | 0.860 | 0.817 | 0.860 | 0.865 | 0.874     |

**Observation:** Average Indic parity improves after continual pretraining, showing that MILA promotes more equitable representation across languages.

---

## Baseline Comparisons

For completeness, we also evaluate strong multilingual baselines:  

- **mT5-XL (7B)**  
- **BLOOMZ-7B**  
- **LLaMA-2-7B**  
- **Gemma-7B**  
- **Mixtral-7B**  
- **Granite-7B**  

Results are provided in the indic mmlu folder.

---

## Conclusion

MILA significantly improves both **absolute performance** and **fairness (Indic parity)** for Qwen3-600M. These results demonstrate that targeted continual pretraining on MILA leads to stronger and more equitable representation of Indic languages.
