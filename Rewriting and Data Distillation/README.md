 ### Downloading and Reproducibility Links Coming within 24 hours.

# Synthetic Augmentation, Rewriting and Data Distillation

> A culturally-grounded data distillation framework leveraging 370M+ Indian personas across 1400+ domains to generate instruction-ready datasets that are linguistically precise and culturally authentic.

---

## Overview

### The Challenge

Large language models and synthetic data pipelines produce vast quantities of text, but this content predominantly reflects Western perspectives, English-centric knowledge, and reasoning patterns. Simple translations preserve linguistic fidelity but fail to capture:

- Cultural context and local reasoning
- Domain-specific nuances essential for Indian applications
- Authentic Indian modes of thought and expression

### Our Solution

A multi-stage distillation framework centered on **Indian virtual personas** that:

- Embeds Indian values and knowledge through persona-driven generation
- Provides cleaner, more efficient access to world knowledge from state-of-the-art models
- Offers domain control and flexibility in data shaping
- Ensures controllable alignment with local cultural and domain-specific needs

**Key Innovation:** The **Indic PersonaHub** — 300M+ Indian personas spanning 1400+ domains, designed to capture diverse Indian identities, values, and domain expertise.

---

## Data Distillation Pipeline

### Architecture Overview

The pipeline employs iterative feedback loops at each stage to ensure only thoroughly vetted and enriched material becomes part of the training corpus.

```
Population Synthesis (370M+ personas)
         ↓
Cultural Compliance Judge → [Recycle if fails]
         ↓
Task Assignment Agent
         ↓
Task Relevance Judge → [Reassign if mismatched]
         ↓
Action Execution (Primary Outputs)
         ↓
Data Validation Judge
         ↓
Specialist Translation Agent
         ↓
Quality Enrichment Agent
         ↓
Data Persistence Layer
```

### Pipeline Stages

#### 1. Population Synthesis
Generate 370M+ personas across 1400+ broad domains, capturing diverse potential identities and expertise.

#### 2. Cultural Compliance Review
Each persona reviewed by cultural compliance judge. Failing personas recycled for regeneration.

#### 3. Task Assignment
Approved personas paired with relevant domains, contexts, and functions by task assignment agent.

#### 4. Task Relevance Evaluation
Persona-task pairs evaluated for logical coherence and meaningfulness. Mismatches sent back for reassignment.

#### 5. Action Execution
Generate primary outputs serving as first substantive data artifacts.

#### 6. Data Validation
Check for factual accuracy, coherence, and overall alignment.

#### 7. Translation & Refinement
Specialist translation agent produces high-quality Indic language outputs or refines stylistic and linguistic properties.

#### 8. Quality Enrichment
Enhance fluency, context, and naturalness before storage.

---

## Indianization of Personas

### Three-Stage Pipeline

Systematically transforms generic or Western-centric personas into contextually Indian personas, ensuring synthetic text aligns with national identity, societal norms, and domain-specific expertise.

### Stage 1: Indianized Persona Generation

Modify existing personas to explicitly reflect Indian cultural values and national alignment while preserving core traits.

**Prompt Template:**
```
Modify the following persona to make it culturally Indian while preserving 
their core personality traits. Ensure the persona remains aligned with Indian 
nationalism, avoids any anti-Indian government stance, and embodies 
patriotism towards India.

{original_persona}

Provide the generated response (strictly in English language) in the 
following key, value format without any header.

Format:
ps: value of Indianized persona | gd_1: Indianized value of general domain (1%) | 
sp_1: Indianized value of specific domain (1%) | gd_01: Indianized value of 
general domain (0.1%) | sp_01: Indianized value of specific domain (0.1%)
```

**Example:** A scientist working on embryonic stem cell research becomes a dedicated Indian scientist whose ethical advocacy is framed through contributions to India's healthcare ecosystem, with domain anchors reflecting Indian policy, ethics, and biomedical priorities.

---

### Stage 2: Thought-Provoking Question Generation

Generate deeply reflective, domain-specific questions tailored to stimulate reasoning in the Indian context.

**Prompt Template:**
```
Craft a single, thought-provoking and mind-triggering question in {domain} 
that inspires deep reflection and invites a broad exploration of ideas, 
perspectives, and reflections, particularly within the Indian context. 
Provide only the question (strictly in English language), without any 
additional commentary or explanation.
```

**Example Output:** *"How should India navigate the ethical complexities of stem cell research and therapy, balancing the potential for groundbreaking medical advancements with the moral considerations surrounding the use of embryonic stem cells, informed consent, and equitable access to treatments?"*

---

### Stage 3: Final Data Generation

Transform enriched persona and question into large-scale text generation task, producing high-quality passages of 900+ words.

**Prompt Template:**
```
You are {persona}. Your role is to engage with users based on your expertise. 
Stay within your domain and maintain the persona's tone and expertise.

# CONTEXT #
The need for this dataset stems from the desire to uphold a standard of 
excellence in English language content within the {domain} field. By compiling 
a diverse range of well-structured and authentic texts, this collection will 
help maintain a rich linguistic resource that supports clarity, readability, 
and contextual accuracy in various forms of communication.

# OBJECTIVE #
I want you to generate text paragraphs strictly in English language with 900+ 
words for {domain} that is easy to read, flows naturally, and sounds like it 
was written by a human. Generated text data should mimic real world data so 
that it can also be used to improve research and innovation. Use clear 
transitions between sentences and paragraphs while maintaining a consistent 
narrative or argument ensuring a logical progression of thought. Ensure the 
writing is engaging and not mechanically repetitive. Question: {question}

# STYLE #
Follow the simple writing style common in communications. Be persuasive yet 
maintain a neutral tone. Avoid sounding too much like a sales or marketing pitch.

# AUDIENCE #
The primary audience is of Indian origin, so content should incorporate cultural 
familiarity, societal norms, and linguistic nuances relevant to Indian readers.

# RESPONSE #
Generate a well-structured and engaging piece of content adhering to the above 
parameters. The writing should feel natural, contextually appropriate, and 
resonate with the target audience.
```

**Example Output:** Comprehensive essay blending scientific reasoning with India's healthcare priorities, ethical frameworks, and aspirations of global leadership.

---

## Expanded QA Extraction Pipeline

Transforms unstructured Indic text into high-quality instruction data through four stages.

### 1. Context-Aware Chunking

- Segment raw text into meaningful spans (1000-4000 tokens)
- Prevent mid-sentence breaks
- Preserve logical coherence
- Ensure each segment is interpretable as standalone unit

### 2. Relevance Checking and Domain Classification

- Validate cultural/societal relevance to Indian context
- Filter out ephemeral or narrowly technical material
- Assign to domains: Healthcare, Finance, History, Culture, BFSI, Education, Governance, Law, News, Sports, Tourism

**Dataset Distribution:**
- 1,121 chunks from wikipedia_indic
- 619 chunks from dharmawiki
- 4,775 chunks from other domains

### 3. Self-Contained Question Generation

Generate fully independent questions:
- General explanation questions
- Commonsense reasoning questions
- Causal reasoning questions
- Open-ended prompts

Each question constructed to stand alone without requiring reference to original text.

### 4. Multi-Fidelity Answer Generation

Two complementary forms:
- **Crisp answers:** Concise response
- **Detailed answers:** 3-5 sentences with explanatory context and elaboration

---

## Dual Methodology for SFT Dataset Generation

### Component 1: Persona-Driven Synthesis

Leverage personas to generate:
- Synthetic long-form articles
- Multi-turn dialogues
- Reasoning-focused responses
- Content embedding cultural, historical, and societal nuances

Ensures data reflects Indian modes of reasoning and domain expertise.

### Component 2: Structured Transformation

Transform unstructured/semi-structured sources into QA datasets:
- OCRed documents
- Transcripts
- Web scrapes

Process: Segmentation → Validation → Domain Classification → Question Generation → Answer Generation

---

## Experimental Results

### SFT Recipe Comparison

| Task | Metric | Open Source SFT | In-house SFT Recipe |
|------|--------|-----------------|---------------------|
| hellaswag | acc_norm | 70.47 | **73.07** |
| hellaswag_hi | acc_norm | 44.01 | **44.59** |
| global_mmlu_full_en | acc | 37.89 | 37.4 |
| global_mmlu_full_hi | acc | 31.43 | **31.65** |
| mmlu_pro | exact_match | 5.23 | **8.73** |
| piqa | acc_norm | 78.24 | **79.22** |
| winogrande | acc | 62.04 | **62.19** |
| truthfulqa_gen | bleu_acc | 35.74 | **37.7** |
| truthfulqa_mc1 | acc | 27.17 | **29.74** |
| cb | acc | 30.36 | **57.14** |
| milu_English | acc | 35.95 | **37.19** |
| milu_Hindi | acc | 28.87 | **32.26** |
| sanskriti_states | acc | 55.13 | **55.91** |

**Key Improvements:**
- **67% improvement** on CommitmentBank (cb): 30.36 → 57.14
- **66% improvement** on MMLU Pro: 5.23 → 8.73
- Consistent gains across Hindi and English benchmarks
- Significant improvement on culturally-specific tasks (milu_Hindi: +11.7%)

---

## Key Insights

1. **Cultural grounding matters:** Persona-driven synthesis outperforms simple translation or Western-centric synthesis
2. **Scale + quality:** 370M personas enable diverse, contextually rich data generation
3. **Iterative validation:** Multiple judge agents ensure only high-quality data enters corpus
4. **Dual approach:** Combining synthetic generation with structured extraction maximizes coverage and depth
5. **Measurable impact:** In-house recipe shows consistent improvements across reasoning, knowledge, and cultural tasks

---

## Data Governance

All personas verified through:
- Cultural compliance checking
- Task relevance validation
- Data quality assessment
- Human expert review for flagged cases

All models used in pipeline verified for high performance on Indic MMLU benchmarks.

---

## Output Scale

**Indic PersonaHub:** 300M+ Indian personas across 1400+ domains

**Generated Data:**
- Long-form articles (900+ words)
- Multi-turn dialogues
- QA pairs with crisp and detailed answers
- Chain-of-Thought reasoning samples
- Cross-lingual transformations

---

*This framework demonstrates that culturally-adaptive synthetic data generation outperforms translation-based approaches for building authentic, contextually-grounded datasets for Indian languages.*
