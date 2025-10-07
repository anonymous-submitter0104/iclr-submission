# ISOB: Indian Synthetic OCR Benchmark – Small-Hard

## Table of Contents

1. [Motivation](#motivation)
2. [What Makes ISOB Unique](#what-makes-isob-unique)
3. [Benchmark Characteristics](#benchmark-characteristics)
4. [Future Benchmark Releases](#future-benchmark-releases)
5. [ISOB Construction Recipe](#isob-construction-recipe)

   * [Input & Output](#input--output)
   * [Step 0: Initialize Seed Corpus](#step-0-initialize-seed-corpus)
   * [Step 1: Hard Page Identification](#step-1-hard-page-identification)
   * [Step 2: Language Selection](#step-2-language-selection)
   * [Step 3: Artifact Taxonomy Extraction](#step-3-artifact-taxonomy-extraction)
   * [Step 4: Synthetic hOCR Augmentation](#step-4-synthetic-hocr-augmentation)
   * [Step 5: hOCR to Visual Conversion](#step-5-hocr-to-visual-conversion)
   * [Step 6: Style Transformation](#step-6-style-transformation)
   * [Step 7: Image Processing Augmentation](#step-7-image-processing-augmentation)
   * [Step 8: Storage & Annotation](#step-8-storage--annotation)
6. [Download ISOB-SMALL-HARD Dataset](#download-isob-small-hard-dataset)
7. [End Result](#end-result)
8. [License & Data Usage](#license--data-usage)

---

## Motivation

The Indian subcontinent has a wealth of localized textual data spanning multiple languages, dialects, and historical scripts. While large volumes of OCR datasets exist for English and other major languages, **authentic Indian data is fragmented, often offline, and hyper-local**, collected through partnerships with governmental and regional institutions under formal MOUs and legal agreements.

This data includes:

* Remote or hand-digitized archives
* Region-specific dialects
* Manuscripts with non-standard layouts, tables, equations, and mixed scripts

These materials are challenging to OCR due to their variability, rarity, and complexity. Every single token is valuable, and preserving their fidelity is crucial for research and model evaluation.

---

## What Makes ISOB Unique

1. **Reverse-Engineered Synthetic Benchmark:**
   Directly releasing original data is often restricted due to copyright and MOU constraints. To make the research community aware of these challenges, we **reverse-engineered the OCR process**:

   * Constructing ground-truth hOCR by embedding multilingual content
   * Rendering hOCR into images/PDFs resembling authentic documents
   * Applying advanced image transformations to emulate manuscript degradation, complex layouts, and other artifacts

2. **Hard-to-OCR Pages:**
   The benchmark emphasizes pages that are inherently difficult to OCR, including:

   * Multi-column layouts
   * Tables, equations, and figures
   * Mixed scripts and languages
   * Dense or overlapping text

3. **Controlled Ground Truth:**
   Unlike web-scraped datasets, we maintain **precise ground truth** via synthetic reconstruction, enabling reliable evaluation using metrics like CER, WER, and F-score.

---

## Benchmark Characteristics

* **Languages Covered:** 22 Indian languages
* **Artifacts:** Tables, math, figures, mixed-language pages
* **Difficulty:** Small, hard-to-OCR dataset
* **Ground Truth:** Full hOCR with language tags and metadata
* **Synthetic Construction:** Designed to emulate real-world complexities

---

## Future Benchmark Releases

1. **Indic-Real-OCR Benchmarks-IROB** (licensed for public release)

   * Difficulty levels: Easy, Medium, Hard
   * Dataset sizes: Small, Medium, Large

2. **Indic-Synthetic-OCR Benchmarks-ISOB**

   * Difficulty levels: Easy, Medium, Hard
   * Dataset sizes: Small, Medium, Large

The goal is to expand the benchmark series while keeping ground truth controlled, enabling reproducible evaluation and method development.

---

## ISOB-SMALL-HARD Construction Recipe

### Input & Output

* **Input:** Seed corpus of OCR’d pages in hOCR format
* **Output:** Synthetic benchmark dataset of hard-to-OCR images with:

  * Ground truth hOCR
  * Language tags
  * Artifact metadata

---

### Step 0: Initialize Seed Corpus

* Use existing OCR’ed pages (JSON/hOCR format) as the starting corpus.

---

### Step 1: Hard Page Identification

* Filter pages based on OCR confidence scores

  * Discard empty or low-text pages
* Use **Qwen-VL-7B** grounded with page hOCR to predict difficulty
* Select pages predicted as **hard-to-OCR**

**Result:** `hOCR_1` (hard page set)

---

### Step 2: Language Selection

* Randomly choose **3–10 languages** from a pool of 22 Indian languages for each page.

---

### Step 3: Artifact Taxonomy Extraction

* Build a taxonomy of “hard artifacts” using LLM guidance:

**Examples of Hard Artifacts:**

* Multi-column layouts
* Dense tables
* Handwriting inserts
* Overlapping scripts
* Reading order complexities
* Equations, figures, pie charts
* Complex tables

---

### Step 4: Synthetic hOCR Augmentation

* Enrich `hOCR_1` using:

  * Selected languages (Step 2)
  * Artifact templates (Step 3)

* Produce `hOCR_2` → serves as ground truth

---

### Step 5: hOCR to Visual Conversion

* Render `hOCR_2` into **PDF/image format**

---

### Step 6: Style Transformation

* Construct a **prompt pool** describing Indian manuscript styles, literature, and domain-specific appearances
* Apply **Qwen image editing** on each page to emulate authentic visual styles

---

### Step 7: Image Processing Augmentation

* Apply low-level transformations to increase OCR difficulty:

  * Orientation changes
  * Contrast/brightness adjustments
  * Noise, blur, distortions

---

### Step 8: Storage & Annotation

* Save final images with metadata:

  * Associated ground truth `hOCR_2`
  * Language tags
  * Style/augmentation metadata

---

## Download ISOB-SMALL-HARD Dataset

This is a **representative sample set** of the full dataset, which will be released with **complete metadata annotations** and an **open-source license** upon paper acceptance.

- [Download Full Benchmark (PARQUET)](https://github.com/anonymous-submitter0104/iclr-submission/tree/main/opensource-release/Indic%20MMLU)

> ⚠️ Please cite this repository if you use the dataset in your research.


---

## End Result

A **structured, multilingual, artifact-rich synthetic OCR benchmark** that captures:

* Hard-to-recognize text cases
* Multi-language content
* Complex visual and structural artifacts

This enables the research community to benchmark OCR models effectively on Indian documents that emulate real-world challenges.

---

## License & Data Usage

* A Representative subset of Synthetic benchmark-ISOB-SMALL-HARD is published in this repository.
* Upon acceptance of the paper, the full dataset will be made available under appropriate licensing.

---
