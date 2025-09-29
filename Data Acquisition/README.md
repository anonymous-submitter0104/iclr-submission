 ### Downloading and Reproducibility Links Coming within 24 hours.
---

# Data Acquisition

This section documents the **acquisition pipeline** for our multilingual pretraining corpus. It covers the **sources of data**, the **collection methodology**, and the **organization schema** applied to ensure reproducibility, integrity, and curriculum-aware structuring.

---

## Overview

We aggregate large-scale corpora from **multi-source web crawling**, **curated open datasets**, and **book/academic repositories**. Our acquisition emphasizes **authentic, curriculum-aligned content** to mitigate linguistic and cultural gaps commonly present in purely synthetic or translated datasets.

**Key Sources**
- **Web Crawl + Open Datasets**
  - Multi-lingual websites, forums, academic repositories
  - >1700 datasets hosted on [Hugging Face](https://huggingface.co)
- **Book Collections**
  - ~1M books from [Archive.org](https://archive.org)
  - 28,500 curriculum-aligned documents from the [National Digital Library of India (NDLI)](https://ndl.iitkgp.ac.in)

---

## Acquisition Methodology

1. **Source Integration**
   - Incorporation of resources inspired by *Pile* [1], *RedPajama* [2], and *C4* [3].
   - Unified crawl + dataset ingestion pipeline with provenance tracking.

2. **Schema-First Cataloging**
   - Every acquired item is labeled along **orthogonal axes**:
     - Language
     - Grade level (for school curricula)
     - Content provider / institution
     - Subject domain (for higher education)
   - Items with cross-listings (e.g., bilingual, multi-grade) are **preserved with multiple metadata tags**.

3. **Deduplication & Integrity**
   - Deduplication performed at the **item-ID level**, avoiding loss of multi-labeled content.
   - Metadata normalization ensures **cross-source compatibility**.

4. **Distribution Reporting**
   - Tabular distributions provided at multiple levels:
     - NDLI **school-level content** (languages, classes, providers)
     - NDLI **higher education** (providers, levels, subjects)
   - These reports enable **coverage quantification** and **balanced sampling**.

5. **Scalable Processing**
   - Pipelines designed for **millions of documents**, including OCR + post-correction workflows for Indic scripts.
   - Week-scale ingestion tasks handled via **robust checkpointing** and **shard-based retries**.


## Steps to Reproduce

 To Add Code Steps Here
