# 🇮🇳 India-Centric Image–Text Pairs Dataset

**(Representative Sample Release)**

### 🧾 High-quality multilingual dataset for OCR and Document-VLM model training

---

## 📚 Table of Contents

* [Overview](#-overview)
* [Motivation](#-motivation)
* [Applications](#-applications)
* [Languages Covered](#-languages-covered-representative-release)
* [Dataset Structure](#-dataset-structure)
* [Download Samples](#-download-representative-samples)
* [Future Release Plan](#-future-release-plan)

---

## 🧭 Overview

The **India-Centric Image–Text Pairs** dataset is a **high-quality multilingual training dataset** designed to advance research in **Optical Character Recognition (OCR)** and **Document–Vision Language Models (Document-VLMs)**.
Each entry consists of an **image** paired with its **corresponding OCR text**, enabling fine-tuning and evaluation of multimodal models for **document understanding**, **text recognition**, and **information extraction** tasks.

---

## 🎯 Motivation

While significant progress has been made in OCR and document-VLM systems, existing benchmarks are largely **English-centric** and fail to represent **India’s linguistic and typographic diversity**.

This dataset bridges that gap by offering:

* Real-world **document images** and **text transcriptions** across multiple Indian languages.
* Complex examples involving **mixed scripts**, **layout variations**, and **natural scanning artifacts**.
* Cleanly aligned image–text pairs suitable for **training high-quality OCR and VLM models**.

---

## ⚙️ Applications

This dataset can act as a **seed dataset** for multiple downstream and foundational tasks, including:

| Task Type                         | Example Use                                |
| --------------------------------- | ------------------------------------------ |
| **OCR-only Training**             | Recognition of multilingual printed text   |
| **VLM-based OCR**                 | Visual understanding and OCR fusion models |
| **Document-VLM Extraction**       | Structured data extraction from documents  |
| **Multilingual Comprehension**    | Cross-language document interpretation     |
| **Translation & Layout Analysis** | Joint text-vision understanding tasks      |

---

## 🌏 Languages Covered (Representative Release)

This release includes **representative samples** for the following Indian languages:

| Language  | Script    |
| --------- | --------- |
| Bengali   | বাংলা     |
| Hindi     | हिन्दी    |
| Kannada   | ಕನ್ನಡ     |
| Malayalam | മലയാളം    |
| Marathi   | मराठी     |
| Sanskrit  | संस्कृतम् |
| Tamil     | தமிழ்     |
| Telugu    | తెలుగు    |

> The dataset has been curated to ensure linguistic balance and visual diversity, showcasing realistic challenges in OCR and document-level understanding.

---

## 🧩 Dataset Structure

Each sample includes:

* 🖼️ **Image** — A cropped or full-page document image containing printed or typed text.
* 🧾 **OCR Text** — Clean, structured machine-readable text corresponding to the image.
* 🏷️ **Metadata** — Includes language, font style, document type, and data source information.

---

## 🗓️ Future Release Plan

* ✅ **This Release:** Representative samples for 8 Indian languages
* 📦 **Full Release (Post-Acceptance):**

  * Coverage of **all 22 official Indian languages**
  * **Detailed metadata tagging**
  * **Open-source licensing and documentation**
  * Integration with **OCR, VLM, and multimodal benchmarks**
