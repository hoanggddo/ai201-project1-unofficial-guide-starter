# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

## Domain
<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
The chosen domain is student-generated reviews of Computer Science professors at George Mason University, focusing on real student experiences with teaching quality, workload, grading difficulty, exams, and project structure.

This knowledge is valuable because official university sources only describe course objectives and syllabi, not the actual student experience. It is also difficult to find through official channels because important decision-making factors such as exam difficulty, fairness of grading, project workload, and teaching style are only shared informally across platforms like RateMyProfessor-style reviews. Students often need to manually browse large volumes of unstructured feedback to compare professors, making it an ideal use case for a retrieval-augmented generation system.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions. Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Yutao Zhong CS112 reviews | Student feedback on CS112 intro programming course | `zhong_cs112.txt` |
| 2 | Yutao Zhong CS367 reviews | Reviews covering workload, exams, and projects | `zhong_cs367.txt` |
| 3 | Yutao Zhong CS310 reviews | Data structures course reviews focusing on exams and projects | `zhong_cs310.txt` |
| 4 | Xu Han CS211 reviews | Object Oriented CS concepts and algorithms course | `han_c211.txt` |
| 5 | Wassim Masri CS310 reviews | Student feedback on lectures, exams, and course structure | `masri_cs310.txt` |
| 6 | Wassim Masri CS321 reviews | Software engineering course reviews focusing on group projects | `masri_cs321.txt` |
| 7 | Alexander Laufer CS405 reviews | Reviews of group-project and writing-heavy CS course | `laufer_cs405.txt` |
| 8 | Jana Kosecka CS483 reviews | Algorithm/theory-heavy course reviews | `kosecka_cs483.txt` |
| 9 | Ahmed Zaman CS112 reviews | Intro CS course reviews with workload and exam feedback | `zaman_cs112_alt.txt` |
| 10 | Ahmed Zaman CS330 reviews | theory-heavy course reviews | `zaman_cs330_alt.txt` |

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
