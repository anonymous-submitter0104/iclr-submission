 ### Downloading and Reproducibility Links Coming within 24 hours.

# Translation Pipeline for Indic Languages

> A robust multi-stage pipeline for generating high-quality parallel corpora across 16 low-resource Indic languages, combining specialist models, generalist LLMs, and human validation.

---

## Overview

High-quality monolingual and parallel corpora remain scarce for Indic languages. Our translation pipeline addresses this gap by:

- Generating parallel corpora enabling cross-lingual transfer from resource-rich to low-resource languages
- Supporting complex domains: mathematics, STEM, formal proofs, and code
- Combining ensemble translation, LLM-based post-correction, and human evaluation
- Handling long-context dependencies through intelligent chunking strategies

**Key Insight:** No single translation model is universally optimal. Specialist systems excel in narrow contexts but lack generalization, while generalist LLMs provide coverage but struggle with low-resource language fidelity.

---

## Pipeline Architecture

### Step 1: Data Augmentation and Diversification

Augment datasets with:
- Parallel data from resource-rich languages
- Complex modalities (code, math, STEM, proofs)
- Diverse domain-specific tasks

**Rationale:** Improves cross-domain generalization and strengthens model reasoning abilities.

---

### Step 2: Initial Translation (Ensemble Generation)

Generate translations using ensembled models:
- **Specialist models** — Domain/language-tuned for technical fidelity
- **Generalist LLMs** — Broad fluency and adaptability

**Observation:** Feeding specialist model outputs to generalist models improves translation quality based on human judgment analysis.

**Output:** Multiple candidate translations per segment.

---

### Step 3: Post-Correction and Quality Enhancement

#### 3.1 Semantic Consensus via LLM-as-Judge

Use strong multilingual LLMs (Qwen-235B, DeepSeek, GPT-OSS) to rank translations based on:
- Semantic fidelity
- Grammatical correctness
- Fluency
- Domain preservation

**Prompt template:**
```
You are a multilingual semantic evaluator.
Input: Source text + multiple candidate translations.
Task: Rank translations for:
(i) semantic fidelity
(ii) grammar/fluency
(iii) technical correctness
Return JSON {best_translation, justification}.
```

#### 3.2 Back-Translation for Robustness

- Translate Indic output back into English
- Compare embeddings with original English source
- Use LLM as judge to finalize similarity assessment

---

### Step 4: Human Evaluation and Finalization

- Low-score cases sent for human verification and post-correction
- 3 language evaluators review initial outputs to guide model selection
- Calibration ensures culturally aligned, domain-sensitive correctness

---

### Step 5: Long-Context Chunking Strategy

For documents with 20K–25K+ tokens:

**Hierarchical chunking approach:**
- Divide texts into contiguous segments based on token counts and logical units
- Provide summaries of preceding segments to maintain continuity
- Include overlapping tokens between consecutive chunks for structured content

**Prompt template:**
```
You are a long-context translator.
Input: Segment of a long document (with overlapping context from previous segment)
Task: Translate into {Indic language}, ensuring continuity with prior segments
Return translation only.
```

**Rationale:** Maintains dependencies across segments, preventing information loss in multi-step reasoning tasks.

---

### Step 6: Consolidation and Verification

- Merge chunked outputs into final translated document
- Validate coherence using LLM reasoning + embedding similarity across boundaries

**Prompt template:**
```
You are a coherence evaluator.
Input: Consecutive translated chunks
Task: Verify continuity of meaning, terminology consistency, and semantic flow
Return verdict: {Consistent, Inconsistent, Requires Edit}.
```

---

### Step 7: Expert Review and Benchmarking

Flag low-confidence cases for human linguist review and benchmark against:
- Semantic LLM scores
- Embedding similarity metrics
- Human evaluation reports

---

## Post-Correction Refinement

LLM-based post-correction repairs:
- Grammatical inconsistencies
- Syntactic and semantic errors
- Morphological variations
- Context preservation issues

**Prompt template:**
```
Role and Context: You are an expert linguist specializing in {language} 
with deep understanding of grammar, syntax, and natural language use.

Task: Transform {language} text that is poorly structured, grammatically 
incorrect, awkwardly translated, or unnatural into well-formed, 
grammatically correct, and natural-sounding {language} text.

Input Text: '{input_text}'

Output Requirements:
- Return complete rephrased text with no omissions wherever needed
- Never return empty responses
- Maintain original language with no English/Hindi mixing
- Focus on grammatical correctness and natural flow
- Do not provide explanations, notes, or meta-commentary
- Keep the length close to the original text
```

**Model Selection:** Only models demonstrating strong performance on Indic MMLU benchmarks are used for post-correction to ensure linguistic proficiency in low-resource languages.

---

## Experimental Results

### Translation Model Performance (FLORES Benchmarks using chrF++)

#### Without Preprocessing and Postprocessing

| Model | As | Be | Gu | Ka | Hi | Mai | Ml | Mr | Ne | Or | Pa | Sa | Sd | Ta | Te |
|-------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| NLLB-200-3.3B | — | 48.58 | 52.10 | 56.87 | 52.67 | 44.08 | 49.35 | 47.03 | 45.93 | 46.05 | 49.48 | 25.28 | 52.49 | 54.37 | 48.24 |
| NLLB-moe-54B | — | 49.86 | 53.30 | 57.03 | 53.08 | 46.63 | 51.47 | 47.85 | 45.10 | 45.34 | 48.75 | 25.56 | 53.46 | 55.72 | 48.71 |
| hunyuan-mt | — | 42.22 | 41.38 | 46.62 | 45.01 | 8.40 | 1.91 | 43.02 | 0.83 | 0.95 | 1.04 | 18.80 | 42.94 | 40.03 | 39.75 |
| deepseek v3.1 Think | 39.10 | 44.30 | 47.95 | 53.12 | 47.56 | 39.59 | 46.86 | 44.80 | 47.23 | 44.34 | 46.80 | 25.37 | 48.90 | 48.68 | 46.05 |
| Llama-4-Maverick-17B | 40.35 | 47.09 | 48.71 | 53.21 | 47.57 | 42.03 | 44.88 | 46.64 | 44.65 | 39.34 | 45.88 | 28.13 | 48.05 | 47.42 | 57.34 |

#### With Preprocessing and Postprocessing

| Model | As | Be | Gu | Ka | Hi | Mai | Ml | Mr | Ne | Or | Pa | Sa | Sd | Ta | Te |
|-------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| IT2 Processed | 48.40 | 51.71 | 55.53 | 58.71 | 54.97 | 49.49 | 55.99 | 51.00 | 56.01 | 52.28 | 51.08 | 30.24 | 56.86 | 58.65 | 50.88 |
| IT2 | 45.10 | 48.67 | 53.38 | 55.62 | 52.26 | 47.04 | 52.23 | 49.33 | 53.42 | 50.47 | 49.82 | 27.70 | 53.03 | 54.77 | 49.19 |

**Language codes:** As (Assamese), Be (Bengali), Gu (Gujarati), Ka (Kannada), Hi (Hindi), Mai (Maithili), Ml (Malayalam), Mr (Marathi), Ne (Nepali), Or (Odia), Pa (Punjabi), Sa (Sanskrit), Sd (Sindhi), Ta (Tamil), Te (Telugu)

---

## Key Findings

- **No universal model:** Specialist and generalist models excel in different contexts
- **Pipeline benefits:** Preprocessing and postprocessing improve chrF++ scores by 3-7 points across languages
- **Ensemble advantage:** Combining specialist + generalist outputs yields higher quality than either alone
- **Long-context handling:** Chunking strategy successfully maintains coherence in complex, multi-step reasoning tasks
- **Human validation:** Critical for low-resource languages where automated metrics may be unreliable

---

## Output Scale

Our pipeline generated coherent, high-fidelity translations across billions of tokens, significantly reducing errors and inconsistencies that arise in single-pass approaches.

---

## Reproducibility

All prompt templates, chunking strategies, and evaluation protocols are provided for reproducibility. Human evaluation guidelines and language-specific post-correction instructions available upon request.

---

*This pipeline demonstrates that carefully designed multi-stage processing outperforms any single translation system for low-resource Indic languages.*
