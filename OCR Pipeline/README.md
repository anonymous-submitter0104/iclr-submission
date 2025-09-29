 ### Downloading and Reproducibility Links Coming within 24 hours.

---

# Indic OCR Pipeline

> A robust multi-stage pipeline for optical character recognition of low-resource Indian languages, designed to handle complex scripts and degraded documents.

---

## Overview

Indic languages face significant digital scarcity, particularly low-resource languages like Maithili and Sindhi. We developed a comprehensive OCR pipeline to process **5–6 million pages** from print materials and scanned books, converting inaccessible texts into machine-readable format.

### Key Challenges

- **Poor scan quality** — 37% of materials exhibited faded ink, irregular printing, and evolving orthographies
- **Complex scripts** — Ligatures, conjunct consonants, and diacritics across Devanagari, Bengali, Tamil, Telugu, and more
- **Layout variation** — Multi-column formats, newspapers, manuscripts, tables, and figures

---

## Pipeline Architecture

### 1. Pre-Processing

- Denoising, binarization, and contrast enhancement
- Super-resolution (SRGAN) for readability improvement
- VLM-based artifact detection (orientation, blur, stamps, illustrations)

**Example prompt:**
```
You are a document analysis system. Identify:
1. Orientation (normal, rotated, upside-down)
2. Noise, blur, watermarks
3. Non-text regions
4. Overall readability score
Return structured JSON.
```

### 2. OCR Generation

- Ensemble of script-specific OCR models
- Generalist VLMs for layout interpretation
- Human-in-the-loop calibration on sampled pages

**Layout detection prompt:**
```
You are an OCR layout assistant. Output:
1. Document layout (columns, tables, figures)
2. Logical reading order
3. Script/language hints
Return as structured JSON.
```

### 3. Post-OCR Enhancement

- Rule-based normalization (dictionary checks, Unicode repair, spacing fixes)
- LLM-based postcorrection for grammar and semantic alignment

### 4. Validation

- hOCR reconstruction with style transfer
- Embedding similarity between original and reconstructed images
- Reasoning-based validation with VLMs
- Trajectory comparison using LLMs for semantic similarity scoring
- Human expert review for flagged cases

---

## ISOB: Indic Synthetic OCR Benchmark

Due to copyright constraints on scanned materials, we created **ISOB-Small**, a synthetic benchmark covering **22 Indian languages**.

### Features

- **110 synthetic pages** with diverse layouts and degradations
- Multi-column layouts, tables, equations, blur, shadows, watermarks, folds, font variation
- Stress-tests for ligatures, conjunct consonants, and diacritics

### Generation Pipeline

1. **Seed Corpus** — Initialize with OCR'd hOCR pages
2. **Hard Page Selection** — Identify difficult pages using confidence scores + VLM classifiers
3. **Language Sampling** — Random selection of 3–10 languages
4. **Artifact Taxonomy** — Extract complex layouts via LLMs
5. **Synthetic Augmentation** — Add multilingual + artifact-rich structures
6. **Visual Rendering** — Convert to images/PDFs
7. **Style Transformation** — Simulate manuscript/book styles
8. **Degradation** — Apply noise, blur, distortions
9. **Annotation** — Store with ground truth hOCR, language tags, metadata

---

## Evaluation

### Metrics

- Character Error Rate (CER)
- Word Error Rate (WER)
- Position-Independent WER (PI-WER)
- Char3-gram F1

### LLM-Assisted Quality Evaluation

Traditional metrics are insufficient post-enhancement. Our framework includes:

- LLM-based quality judging (OCR vs. ground truth)
- Multilingual embedding similarity for semantic fidelity
- Back-translation to English for cross-lingual alignment
- BLEU, ROUGE, CHRF++ for translation-level evaluation
- Image embedding validation for reconstructed pages

### Key Findings

- VLMs provide coverage but hallucinate in Indic scripts
- Specialist OCR models outperform after preprocessing + postcorrection
- Pretraining on processed OCR text yields smoother convergence vs. raw OCR

---

## Dataset Release

**ISOB-Small** (22 languages, 110 pages) will be released publicly for research purposes.

Includes:
- Synthetic generation recipes
- Augmentation scripts
- Ground truth annotations
- Reproducibility documentation

Future releases planned for **Indic-Real-OCR** and **Indic-Synthetic-OCR** variants.

---

## Key Insights

1. OCR quality depends critically on data availability and processing pipelines
2. Iterative refinement (preprocessing → OCR → postcorrection → validation) is essential
3. Synthetic benchmarks fill critical gaps in Indic OCR research
4. Human-in-the-loop validation ensures quality for low-resource scenarios

---

*This work addresses the digital divide for low-resource Indian languages through innovative OCR techniques and reproducible benchmarking.*
