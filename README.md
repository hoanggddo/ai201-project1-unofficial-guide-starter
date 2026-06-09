# The Unofficial Guide — Project 1

---

## Domain

This system covers student-generated reviews of Computer Science professors at George Mason University, focusing on real student experiences with teaching quality, workload, grading difficulty, exams, and project structure.

This knowledge is valuable because official university sources only describe course objectives and syllabi, not the actual student experience. Important decision-making factors such as exam difficulty, fairness of grading, project workload, and teaching style are only shared informally across platforms like RateMyProfessor-style reviews. Students often need to manually browse large volumes of unstructured feedback to compare professors, making it an ideal use case for a retrieval-augmented generation system.

---

## Document Sources

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Yutao Zhong CS112 reviews | Student feedback on CS112 intro programming course | `zhong_cs112.txt` |
| 2 | Yutao Zhong CS367 reviews | Reviews covering workload, exams, and projects | `zhong_cs367.txt` |
| 3 | Yutao Zhong CS310 reviews | Data structures course reviews focusing on exams and projects | `zhong_cs310.txt` |
| 4 | Xu Han CS211 reviews | Object Oriented CS concepts and algorithms course | `han_cs211.txt` |
| 5 | Wassim Masri CS310 reviews | Student feedback on lectures, exams, and course structure | `masri_cs310.txt` |
| 6 | Wassim Masri CS321 reviews | Software engineering course reviews focusing on group projects | `masri_cs321.txt` |
| 7 | Alexander Laufer CS405 reviews | Reviews of group-project and writing-heavy CS course | `laufer_cs405.txt` |
| 8 | Jana Kosecka CS483 reviews | Algorithm/theory-heavy course reviews | `kosecka_cs483.txt` |
| 9 | Ahmed Zaman CS112 reviews | Intro CS course reviews with workload and exam feedback | `zaman_cs112_alt.txt` |
| 10 | Ahmed Zaman CS330 reviews | Theory-heavy course reviews | `zaman_cs330_alt.txt` |

---

## Chunking Strategy

**Chunk size:** One review per chunk — no fixed character or token limit.

**Overlap:** None (0 overlap).

**Why these choices fit your documents:** Each review is a self-contained unit of opinion: it covers one professor, one course, and one student's complete experience. Splitting a review mid-sentence would break the semantic unit and force the embedding model to represent an incomplete thought. Because reviews vary in length (some are 2 sentences, some are 8+), a fixed character split would either fragment short reviews or truncate long ones. Treating each review as one chunk preserves the full context the LLM needs to generate a grounded answer.

Overlap was not used because there are no meaningful boundaries to straddle — each review is independent of the next. Overlap is most useful when a key fact might span two adjacent text windows; that doesn't apply here since no single fact crosses review boundaries.

**Preprocessing:** Each `.txt` file was parsed using regex to extract the `Professor:` and `Course:` header fields. Reviews were split on `Review N` delimiters. Chunks shorter than 50 characters and chunks containing the string "No meaningful review content provided" were discarded.

**Final chunk count:** 93 chunks across 10 documents.

---

## Sample Chunks

Below are 5 representative chunks from the corpus, each shown with its source file.

**Chunk 1** — `zaman_cs112_alt.txt`
```
Professor: Ahmed Zaman
Course: CS112
Review: Review 3

The course was manageable if you kept up with ZyBooks and attended labs. Lectures were okay but not the best way to learn programming if you have zero experience. The exams were fair and matched what was covered in class. Difficulty: 1/5.
```

**Chunk 2** — `masri_cs321.txt`
```
Professor: Wassim Masri
Course: CS321
Review: Review 5

The group project was the biggest challenge. Deadlines felt rushed and coordinating with teammates was harder than the actual coding. Wes was available during office hours and graded fairly, but the project itself was stressful. Quizzes were harder than expected.
```

**Chunk 3** — `laufer_cs405.txt`
```
Professor: Alexander Laufer
Course: CS405
Review: Review 2

Very heavy workload. Dense readings every week, lectures that go off-topic, and a group project with an unrealistically short deadline. The writing component was graded strictly. Not recommended if you're taking other heavy courses at the same time.
```

**Chunk 4** — `zhong_cs112.txt`
```
Professor: Yutao Zhong
Course: CS112
Review: Review 7

Lectures can be dry and repetitive — a lot of it overlaps with the textbook. That said, the structure of the course is clear and the projects are reasonable if you start early. Heavy workload overall but manageable with consistency.
```

**Chunk 5** — `kosecka_cs483.txt`
```
Professor: Jana Kosecka
Course: CS483
Review: Review 4

The course was poorly organized. Explanations during lecture were unclear and the projects felt disconnected from what was taught. Ended up relying heavily on outside resources to understand the material. Would not recommend unless you are very self-motivated.
```

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`, running locally.

**Why this model:** It runs entirely locally with no API key or rate limits, making it practical for development. It performs well on short, opinionated text like student reviews and produces 384-dimensional embeddings that are fast to generate and store.

**Production tradeoff reflection:** For a real deployment, I would weigh several factors. A larger model like `text-embedding-3-large` (OpenAI) or `e5-large` would likely produce more accurate embeddings for domain-specific language (e.g., course-specific jargon like "ZyBooks" or professor nicknames like "Wes"), but would introduce API latency and cost per query. If the system needed to support international students, multilingual embedding models like `paraphrase-multilingual-MiniLM-L12-v2` would be necessary. Context length would matter more if reviews were longer — MiniLM has a 256-token limit, which is fine for short reviews but would truncate longer documents. For a high-traffic production system, I would also evaluate whether to host the model locally (lower latency, no API cost) or use a hosted API (easier scaling, no GPU required).

---

## Retrieval Test Results

**Query 1: "Which professor has the easiest exams?"**

Top retrieved chunks:
- `zaman_cs112_alt.txt` — "Exams were fair and matched what was covered in class. Difficulty: 1/5."
- `han_cs211.txt` — "Exams were straightforward and easier than the assignments."
- `zaman_cs330_alt.txt` — "Exams closely match the practice exams provided."

These chunks are relevant because they all directly describe exam difficulty. The query phrase "easiest exams" semantically matched review language about fairness, low difficulty ratings, and exam-practice alignment — not just keyword overlap.

**Query 2: "Which classes have heavy workload?"**

Top retrieved chunks:
- `zhong_cs112.txt` — "Heavy workload overall — projects, labs, homework, and online readings."
- `laufer_cs405.txt` — "Very heavy workload. Dense readings every week."
- `han_cs211.txt` — "Reading workload is heavy at the beginning of the semester."

These chunks are relevant because they each explicitly describe workload volume in a specific course, which is exactly what the query asks for. The model correctly matched "heavy workload" across differently phrased reviews.

**Query 3: "Which professors have bad or boring lectures?"**

Top retrieved chunks:
- `zhong_cs112.txt` — "Lectures can be dry and repetitive."
- `kosecka_cs483.txt` — "Explanations during lecture were unclear."
- `masri_cs310.txt` — "Lectures were hard to follow."

These are relevant matches. "Boring" and "dry/repetitive" are not the same word, but the embedding model correctly recognized them as semantically similar — a good example of semantic search working as intended.

---

## Grounded Generation

**System prompt grounding instruction:**

```
You are a university assistant that answers questions about professors based solely on student reviews.

RULES:
- Answer ONLY using the provided context. Do not add outside knowledge.
- If the question names a specific professor, use only reviews for that professor.
- If multiple reviews disagree, present each perspective separately — do not average or summarize them into one conclusion.
- Do not use phrases like "overall", "generally", or "in conclusion".
- Do not number or label individual reviews in your answer.
- Do not expose source filenames or internal metadata to the user.
- If the context does not contain enough information to answer, respond with:
  "I don't have enough information from the student reviews to answer that."
```

**How source attribution is surfaced in the response:** Source filenames are collected from the metadata of retrieved chunks and returned as a separate `sources` field in the `generate_answer` function. The Gradio interface displays them in a dedicated "Sources" text box below the answer. Source filenames are passed to the LLM as part of the context block but the system prompt instructs the model not to expose them in the answer text — attribution is surfaced programmatically, not left to the model to generate.

**Out-of-scope query example:**

Query: *"What is the best gym on campus?"*

System response: *"I don't have enough information from the student reviews to answer that."*

This confirms grounding is working — the system did not draw on general GMU knowledge to answer a question outside the document corpus.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which CS professor is best for beginners? | Yutao Zhong is described as supportive and good for intro students | System returned mixed results: Zaman's CS112 was noted as manageable for beginners with effort; Zhong's CS112 had heavy workload notes but clear structure; no professor was clearly ranked best for beginners | Partially relevant | Partially accurate |
| 2 | Which professors have the hardest projects? | Masri or Zhong for CS310/CS367 | System correctly identified Laufer (CS405) and Kosecka (CS483) as having difficult projects, but did not surface Zhong's CS367 project difficulty | Partially relevant | Partially accurate |
| 3 | Which professor has the easiest exams? | Zaman and Zhong described as having fair/straightforward exams | System correctly returned Zaman CS112 (difficulty 1/5) and Han CS211 (exams easier than assignments) with accurate citations | Relevant | Accurate |
| 4 | Which classes have heavy workload? | CS310 and CS321 described as heavy | System returned CS112 (Zhong), CS405 (Laufer), and CS211 (Han) as heavy — missed CS321 and CS310 specifically | Partially relevant | Partially accurate |
| 5 | Which professors have bad or boring lectures? | Masri and Kosecka described as boring/unclear | System correctly identified Zhong (dry/repetitive), Kosecka (unclear), and Masri (hard to follow) | Relevant | Accurate |

---

## Failure Case Analysis

**Question that failed:** "Which professors have the hardest projects?"

**What the system returned:** The system surfaced Laufer (CS405 group project, short deadline) and Kosecka (CS483 disorganized projects) as having hard projects, but did not return Zhong's CS367 reviews, which were expected to appear based on the planning.md spec.

**Root cause (tied to a specific pipeline stage):** The failure is in retrieval. The query "hardest projects" matched chunks that used the words "challenging," "difficult," and "disorganized" in the context of projects — but Zhong's CS367 reviews may have described project difficulty using different phrasing (e.g., "time-consuming" or "started early") that didn't score as highly in semantic similarity. Because `all-MiniLM-L6-v2` is a general-purpose model not fine-tuned on course review language, it doesn't recognize that "start early or you'll fall behind" implies project difficulty. The relevant chunks existed in the corpus but ranked below the top-k cutoff of 4.

**What you would change to fix it:** Increase top-k during retrieval (e.g., from 4 to 8) and add a re-ranking step that scores retrieved chunks against the query a second time using a cross-encoder model. Alternatively, expanding the query before embedding ("hardest projects" → "difficult assignments, time-consuming projects, heavy project workload") could pull in more relevant chunks.

---

## Spec Reflection

**One way the spec helped during implementation:** The chunking strategy in planning.md — one review per chunk, no overlap — directly shaped the ingestion logic in `ingest.py`. Because the spec was written before any code, the regex-based review splitter was built specifically to preserve each review as a unit rather than applying a generic character-count split. This avoided a common RAG failure where a review's conclusion ends up in a different chunk from its premise, making neither chunk independently useful for retrieval.

**One way implementation diverged from the spec, and why:** The spec anticipated top-k of 4 for retrieval. During implementation, `rag.py` was updated to retrieve k=10 first, then filter by professor name, then truncate to 4. This divergence was necessary because a flat k=4 query often returned chunks from unrelated professors when the question named a specific one — the professor name filter had to operate on a larger candidate pool to be effective. The spec didn't anticipate the need for a post-retrieval filtering step.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* The Chunking Strategy and Documents sections from planning.md, plus the requirement that each review be treated as one chunk with professor/course metadata preserved.
- *What it produced:* A Python script using `re.split(r"Review\s+\d+", content)` to split each file, with a loop that assembled chunk dictionaries containing `professor`, `course`, `text`, and `source` fields.
- *What I changed or overrode:* The original generated code had a nested loop bug — `re.split` was being called again inside the `for review in reviews` loop, reprocessing every file's content on each iteration. This caused every chunk to be duplicated N times. The fix was to move the split outside the loop and rename the variable to `parts` to avoid the overwrite.

**Instance 2**

- *What I gave the AI:* The system prompt requirements (grounding, no outside knowledge, per-professor filtering, source attribution) and the Gradio interface skeleton from the project spec.
- *What it produced:* A `rag.py` with a `generate_answer` function and a `format_context` function, plus a working `app.py` with Gradio `Blocks` layout.
- *What I changed or overrode:* The generated `generate_answer` returned the raw `ChatCompletion` object instead of `response.choices[0].message.content`, which caused Gradio to display the entire API response object as a string. The fix was to extract the text content explicitly. Additionally, the `Groq` client was instantiated twice at the top of the file — one instance was removed.