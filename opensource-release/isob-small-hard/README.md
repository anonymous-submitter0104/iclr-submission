# 📄 ISOB Dataset – Representative Sample Release (SMALL-HARD)

**Note:** This is a **representative subset** of the full ISOB dataset. The **complete dataset**, including all images, OCR files, and metadata, will be released upon paper acceptance.

---

## 📚 Table of Contents

* [Overview](#-overview)
* [Motivation](#-motivation)
* [Dataset Structure](#-dataset-structure)
* [Languages Covered](#-languages-covered)
* [Files in This Release](#-files-in-this-release)
* [Language Diversity](#-language-diversity)
* [Usage](#-usage)

---

## 🧭 Overview

The **ISOB dataset** is a **high-quality, India-centric multilingual OCR dataset** created to advance research in **document understanding, OCR, and multilingual Document-VLM systems**.

Each sample consists of:

* A **document image** (possibly containing multiple languages)
* The corresponding **OCR transcription** in text format

This representative release contains a **subset of image–text pairs**, showcasing documents with multiple Indian languages in a single page.

---

## 🎯 Motivation

The Indian subcontinent has a wealth of localized textual data spanning multiple languages, dialects, and historical scripts. While large volumes of OCR datasets exist for English and other major languages, authentic Indian data is fragmented, often offline, and hyper-local, collected through partnerships with governmental and regional institutions under formal MOUs and legal agreements.

This data includes:

* Remote or hand-digitized archives
* Region-specific dialects
* Manuscripts with non-standard layouts, tables, equations, and mixed scripts

These materials are **challenging to OCR** due to their variability, rarity, and complexity. Every single token is valuable, and preserving their fidelity is crucial for research and model evaluation.

The **ISOB dataset** addresses these gaps by:

* Capturing **real-world, multi-language document layouts**
* Providing **aligned OCR text for supervised learning**
* Supporting **evaluation and benchmarking** of multilingual OCR and VLM systems

---

## 🧩 Dataset Structure

For each document in the dataset:

| Component              | Description                                                                          |
| ---------------------- | ------------------------------------------------------------------------------------ |
| Image File             | Document image (.jpg)                                                                |
| OCR File               | Corresponding OCR transcription (.txt)                                               |
| File Naming Convention | Indicates the languages present (e.g., `hocr_assamese_bodo_maithili_urdu_v0141.txt`) |

The **file name encodes** which languages are present in that image, allowing easy filtering or language-specific experiments.

---

## 🌏 Languages Covered

The dataset includes **major Indian languages**, with multiple languages sometimes present in a single document:

* Assamese
* Bengali
* Bodo
* Dogri
* Gujarati
* Hindi
* Kannada
* Kashmiri
* Konkani
* Maithili
* Malayalam
* Manipuri
* Marathi
* Nepali
* Odia
* Punjabi
* Sanskrit
* Santali
* Sindhi
* Tamil
* Telugu
* Urdu

> This release provides a representative subset; the full dataset will cover **all 22 Indian languages**.

---

## 📂 Files in This Release

Below are example files included in this release:

| Image File                                                               | OCR Text File                                           | Languages Present                          |
| ------------------------------------------------------------------------ | ------------------------------------------------------- | ------------------------------------------ |
| `hocr_assamese_bodo_maithili_urdu_v0141_edited_gpu4_s4044.jpg`           | `hocr_assamese_bodo_maithili_urdu_v0141.txt`            | Assamese, Bodo, Maithili, Urdu             |
| `hocr_assamese_kannada_odia_v0131_edited_gpu2_s2051.jpg`                 | `hocr_assamese_kannada_odia_v0131.txt`                  | Assamese, Kannada, Odia                    |
| `hocr_bengali_hindi_maithili_v0008_edited_gpu0_s43.jpg`                  | `hocr_bengali_hindi_maithili_v0008.txt`                 | Bengali, Hindi, Maithili                   |
| `hocr_gujarati_maithili_odia_marathi_v0082_edited_gpu0_s49.jpg`          | `hocr_gujarati_maithili_odia_marathi_v0082.txt`         | Gujarati, Maithili, Odia, Marathi          |
| `hocr_gujarati_sanskrit_marathi_assamese_v0006_edited_gpu4_s4043.jpg`    | `hocr_gujarati_sanskrit_marathi_assamese_v0006.txt`     | Gujarati, Sanskrit, Marathi, Assamese      |
| `hocr_hindi_assamese_telugu_santali_v0139_edited_gpu4_s4048.jpg`         | `hocr_hindi_assamese_telugu_santali_v0139.txt`          | Hindi, Assamese, Telugu, Santali           |
| `hocr_hindi_dogri_assamese_maithili_v0085_edited_gpu1_s1043.jpg`         | `hocr_hindi_dogri_assamese_maithili_v0085.txt`          | Hindi, Dogri, Assamese, Maithili           |
| `hocr_hindi_manipuri_telugu_malayalam_sindhi_v0145_edited_gpu0_s46.jpg`  | `hocr_hindi_manipuri_telugu_malayalam_sindhi_v0145.txt` | Hindi, Manipuri, Telugu, Malayalam, Sindhi |
| `hocr_hindi_odia_santali_maithili_malayalam_v0101_edited_gpu4_s4049.jpg` | `hocr_hindi_odia_santali_maithili_malayalam_v0101.txt`  | Hindi, Odia, Santali, Maithili, Malayalam  |
| `hocr_hindi_santali_sanskrit_v0002_edited_gpu2_s2045.jpg`                | `hocr_hindi_santali_sanskrit_v0002.txt`                 | Hindi, Santali, Sanskrit                   |
| `hocr_kannada_marathi_nepali_hindi_v0026_edited_gpu1_s1050.jpg`          | `hocr_kannada_marathi_nepali_hindi_v0026.txt`           | Kannada, Marathi, Nepali, Hindi            |
| `hocr_kannada_sanskrit_konkani_v0012_edited_gpu1_s1045.jpg`              | `hocr_kannada_sanskrit_konkani_v0012.txt`               | Kannada, Sanskrit, Konkani                 |
| `hocr_kashmiri_bengali_odia_v0040_edited_gpu7_s7042.jpg`                 | `hocr_kashmiri_bengali_odia_v0040.txt`                  | Kashmiri, Bengali, Odia                    |
| `hocr_kashmiri_bengali_sindhi_v0071_edited_gpu3_s3045.jpg`               | `hocr_kashmiri_bengali_sindhi_v0071.txt`                | Kashmiri, Bengali, Sindhi                  |
| `hocr_kashmiri_kannada_manipuri_santali_v0074_edited_gpu7_s7048.jpg`     | `hocr_kashmiri_kannada_manipuri_santali_v0074.txt`      | Kashmiri, Kannada, Manipuri, Santali       |
| `hocr_kashmiri_konkani_odia_v0019_edited_gpu0_s44.jpg`                   | `hocr_kashmiri_konkani_odia_v0019.txt`                  | Kashmiri, Konkani, Odia                    |
| `hocr_kashmiri_odia_gujarati_sindhi_v0083_edited_gpu2_s2043.jpg`         | `hocr_kashmiri_odia_gujarati_sindhi_v0083.txt`          | Kashmiri, Odia, Gujarati, Sindhi           |
| `hocr_kashmiri_santali_hindi_v0011_edited_gpu0_s54.jpg`                  | `hocr_kashmiri_santali_hindi_v0011.txt`                 | Kashmiri, Santali, Hindi                   |
| `hocr_konkani_assamese_urdu_sindhi_v0129_edited_gpu5_s5048.jpg`          | `hocr_konkani_assamese_urdu_sindhi_v0129.txt`           | Konkani, Assamese, Urdu, Sindhi            |
| `hocr_konkani_gujarati_bodo_bengali_v0130_edited_gpu7_s7052.jpg`         | `hocr_konkani_gujarati_bodo_bengali_v0130.txt`          | Konkani, Gujarati, Bodo, Bengali           |
| `hocr_konkani_malayalam_bodo_hindi_v0013_edited_gpu7_s7050.jpg`          | `hocr_konkani_malayalam_bodo_hindi_v0013.txt`           | Konkani, Malayalam, Bodo, Hindi            |
| `hocr_konkani_punjabi_hindi_sanskrit_v0033_edited_gpu6_s6043.jpg`        | `hocr_konkani_punjabi_hindi_sanskrit_v0033.txt`         | Konkani, Punjabi, Hindi, Sanskrit          |
| `hocr_konkani_sindhi_telugu_v0075_edited_gpu3_s3042.jpg`                 | `hocr_konkani_sindhi_telugu_v0075.txt`                  | Konkani, Sindhi, Telugu                    |
| `hocr_maithili_dogri_tamil_v0102_edited_gpu4_s4052.jpg`                  | `hocr_maithili_dogri_tamil_v0102.txt`                   | Maithili, Dogri, Tamil                     |
| `hocr_maithili_gujarati_tamil_bodo_v0105_edited_gpu1_s1051.jpg`          | `hocr_maithili_gujarati_tamil_bodo_v0105.txt`           | Maithili, Gujarati, Tamil, Bodo            |

> Full file listing is available in the repository directory.

---

## 🔢 Language Diversity

The representative release spans multiple languages per document. Below is the **frequency of languages across all released files**:

Perfect! Here's an enhanced version of the **Language Diversity heatmap** using **colored Unicode bars** in GitHub Markdown, which will make the heatmap visually appealing and easy to interpret:

```markdown

The representative release spans multiple languages per document. Below is the **frequency of languages across all released files**:

- Hindi:      🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥 11 files  
- Konkani:    🟧🟧🟧🟧🟧🟧🟧 7 files  
- Assamese:   🟨🟨🟨🟨🟨🟨 6 files  
- Maithili:   🟩🟩🟩🟩🟩🟩 6 files  
- Odia:       🟦🟦🟦🟦🟦🟦 6 files  
- Gujarati:   🟪🟪🟪🟪🟪 5 files  
- Santali:    🟫🟫🟫🟫🟫 5 files  
- Sindhi:     ⬛⬛⬛⬛⬛ 5 files  
- Bengali:    🟩🟩🟩🟩 4 files  
- Bodo:       🟦🟦🟦🟦 4 files  
- Kannada:    🟧🟧🟧🟧 4 files  
- Sanskrit:   🟥🟥🟥🟥 4 files  
- Telugu:     🟪🟪🟪 3 files  
- Malayalam:  🟫🟫🟫 3 files  
- Urdu:       ⬛⬛ 2 files  
- Dogri:      🟨🟨 2 files  
- Tamil:      🟩🟩 2 files  
- Kashmiri:   🟦 1 file  
- Nepali:     🟧 1 file  
- Punjabi:    🟥 1 file  
```

> This **visual representation** conveys both the **diversity** and **distribution** of languages across the representative subset.

---

## 🛠️ Usage

* Each OCR file corresponds **one-to-one** with its image.
* Use the OCR text for **training or fine-tuning OCR models**.
* Ideal for **multilingual Document-VLM pretraining**, **evaluation**, and **benchmarking**.

