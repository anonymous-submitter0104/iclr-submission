# Indic Persona Hub — Representative Sample Release

> **Note:** This release contains a **20 Million** diverse India-centric virtual personas. The complete dataset will be made publicly available upon paper acceptance.

---

## What this repo contains

A representative sample release of the *Indic Persona Hub* — a large, India-centric collection of synthetic virtual personas designed for research in NLP, personalization, synthetic data generation, dataset augmentation, and socially-aware ML. This bundle contains 20,000,000 synthetic persona records spread across many India-relevant domains (see distribution below). Files are provided in Apache Parquet (`.parquet`) for columnar storage and fast reads.

---

## Domain distribution (provided personas)

Selected 20,000,000 Personas across 90633 domain buckets.
Top domain distribution:

| Domain            |   Count |
| ----------------- | ------: |
| Indian            | 100,000 |
| social            | 100,000 |
| design            | 100,000 |
| education         | 100,000 |
| business          | 100,000 |
| water             | 100,000 |
| mathematics       | 100,000 |
| ancient           | 100,000 |
| international     | 100,000 |
| statistical       | 100,000 |
| computer_engineer | 100,000 |
| marine            | 100,000 |
| medicine          | 100,000 |
| nutrition         | 100,000 |
| vedic             | 100,000 |
| pediatric         | 100,000 |
| nuclear           | 100,000 |
| computer_science  | 100,000 |
| urban             | 100,000 |
| data_science      | 100,000 |
| conservation      | 100,000 |
| hardware          | 100,000 |
| public            | 100,000 |
| military          | 100,000 |
| space             | 100,000 |
| sustainable       | 100,000 |
| environmental     | 100,000 |
| indigenous        | 100,000 |
| traditional       | 100,000 |
| epidemiology      | 100,000 |

---

## How personas were created (high level)

We used two complementary strategies inspired by large-scale synthetic persona work (e.g., approaches discussed in Tencent AI Labs' *Scaling Synthetic Data Creation*):

### 1. Text-to-Persona

We prompt large LLMs with India-centric web texts and open-source corpora. From an input text (article, forum post, news piece, blog, domain document), the LLM is prompted to infer *a plausible persona* — a set of demographic, professional, cultural and interest attributes that would be likely to read/write/like/dislike that text. Because web text is massive and covers many niche topics, Text-to-Persona scales to create wide, diverse persona sets.

### 2. Persona-to-Persona

Text-to-Persona can under-represent low-visibility groups (e.g., children, informal workers, behind-the-scenes roles). Persona-to-Persona derives new personas by applying relationship and role transformations (e.g., family relations, occupational hierarchies, subordinate/supervisor roles) from base personas. This supplements gaps and improves coverage of low-visibility or relational personas.

---

## Persona formats in this release

We provide personas in Apache Parquet (`.parquet`). The `.parquet` files are columnar and efficient for large-scale analytics and fast reads using tools like `pandas`, `pyarrow`, or big-data engines.

### A. `jsonl` (detailed schema)

The canonical JSONL schema used elsewhere in the repo includes many fields (see `schema.json`) such as `id`, `persona_description`, `domain`. This schema is suitable for persona-conditioned generation and fine-grained filtering.

### B. `parquet` (compact sample format)

Some downstream pipelines and snapshots use a compact Parquet schema with fewer columns. The Parquet snapshot included in this release uses the following minimal columns (example):

* `id` — unique identifier (UUID string)
* `persona` — a single long-form text describing the synthetic persona (often combining name + description + attributes in one paragraph)
* `domain` — domain label (string)

#### Example record from the `.parquet` file

```json
{
  "id": "0e0ed30a-90e8-4759-943e-6314313d2a30",
  "persona": "A student enrolled in the Indian History and Culture course at Delhi University, who is deeply interested in Indian history and is eager to engage with the diverse perspectives offered by the course readings. This student is likely to have a strong interest in the Indian Independence Movement, the framing of the Indian Constitution, and the early years of the Indian Republic, as well as various themes of the post-independence era. They may also be interested in the history of colonial rule, the socio-political reforms during the British era, and the impact of the freedom struggle on modern India. This student is likely to have a passion for discussing themes of unity in diversity, the role of religion and culture in shaping Indian society, the struggle for self-rule, and the vision of a progressive and inclusive India. They are likely to be well-versed in the concepts and theories related to Indian history and culture, and embody a strong sense of patriotism and pride in India's rich heritage and achievements.",
  "domain": "Indian history"
}
```

**Note:** This Parquet format purposely keeps the persona consolidated into one `persona` column for compactness and to simplify certain downstream use-cases (indexing, search, vectorization, clustering).

---

## Example usage (Parquet)

Fast streaming example using `pyarrow.dataset` for large-scale scans:

```python
import pyarrow.dataset as ds

dataset = ds.dataset("/path/to/indic_personas_sample.parquet", format="parquet")
scanner = dataset.scanner(columns=["id", "persona", "domain"], batch_size=10000)
for batch in scanner.scan_batches():
    table = batch.to_pandas()
    # process table in-memory
    # e.g., vectorize persona text for clustering or indexing
```

---

## Persona format (notes on style)

* The `.parquet` `persona` column often contains a longer, free-form paragraph combining background, interests, values, and likely discussion topics. This format is intentionally human-readable to suit search, retrieval, and embedding pipelines.

---

## Guiding principles & stewardship

* **India-centric, respectful:** personas were designed to reflect India's cultural, linguistic and regional diversity while avoiding stereotypes and maintaining respect for cultural sensitivities.
* **No real individuals:** personas are synthetic constructs and do not represent real identifiable persons.
* **Minimal identifying detail:** avoid unnecessary personally identifiable information (PII). The release contains synthetic demographic and occupational attributes suitable for research.
* **Transparent provenance:** each persona includes `synth_method` metadata (e.g., `text_to_persona`, `persona_to_persona`) and a `confidence_score` when available.

---

## Limitations & ethical considerations

* **Synthetic bias:** LLM-based generation may inherit biases present in source texts and models. Use caution when deploying persona-conditioned systems in high-stakes settings.
* **Coverage gaps:** despite large scale, some fine-grained local communities or marginal groups may be under-represented.
* **Not for targeted manipulation:** dataset is intended for research, benchmarking, and benign personalization tasks. Do not use to facilitate targeted social manipulation, harassment, or unlawful profiling.
* **Responsible use:** we recommend dataset consumers run fairness and safety checks appropriate to their application and consult domain experts for deployments affecting real people.

---



