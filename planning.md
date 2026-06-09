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
One review per chunk. No fixed token or character limit.

**Overlap:**  
None (0 overlap)

**Reasoning:**  
Each review already contains a complete opinion about a professor and course. It includes things like rating, tags, and feedback in one place. Splitting a review would break context and make it harder for the model to understand the full meaning. Because of this, it makes more sense to treat each review as one full chunk instead of cutting it up.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**  
sentence-transformers `all-MiniLM-L6-v2`

**Top-k:**  
4

**Production tradeoff reflection:**  
In a real system, I would think about accuracy, speed, and cost. Bigger models usually understand text better, but they are slower and more expensive. Smaller models like MiniLM are fast and work well for short texts like reviews.

For top-k, 4 chunks feels like a good balance. If k is too low, the system might miss useful reviews. If k is too high, it will bring in unrelated reviews and confuse the answer.

If this were a production system, I would also consider using a stronger embedding model for better accuracy, but only if performance and cost were acceptable.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Which CS professor is best for beginners? | Yutao Zhong is described as supportive, patient, and good for intro students. |
| 2 | Which professors have the hardest projects? | CS310 and CS483 professors like Masri or Kosceka are described as having difficult projects. |
| 3 | Which professor has the easiest exams? | Yutao Zhong and Ahmed Zaman are described as having fair and straightforward exams. |
| 4 | Which classes have heavy workload? | CS405 and CS211 are described as having heavy workload and group projects. |
| 5 | Which professors have bad or boring lectures? | Wassim Masri and Jana Kosecka are often described as having boring or unclear lectures. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Some reviews are not formatted the same way, so parsing them might miss fields like tags or grades. This could affect retrieval quality.

2. Some reviews mix positive and negative comments in the same text. This might confuse the model when trying to decide overall sentiment.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, Mermaid, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

Documents (.txt files) → Ingestion (Python file loader) → Chunking (1 review = 1 chunk) → Embeddings (sentence-transformers) → Vector Store (ChromaDB) → Top-k Retrieval → LLM → Final Answer with citations

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
I will use ChatGPT or Copilot to help write a Python script that loads all my TXT files and turns them into structured review objects. I will give it my chunking strategy so it knows each review should stay as one chunk. I will check that no review is split and all fields (professor, course, grade, tags, review text) are preserved.
**Milestone 4 — Embedding and retrieval:**
I will use AI to help set up ChromaDB and embeddings using sentence-transformers. I will provide my retrieval plan (MiniLM model and top-k = 4). I will test it by searching simple queries and checking if the right professors and reviews come back.
**Milestone 5 — Generation and interface:**
I will use AI to help build the prompt and query interface. I will give it the format of retrieved chunks and ask it to generate answers only using that data. I will verify it by making sure responses do not include anything outside the retrieved reviews.