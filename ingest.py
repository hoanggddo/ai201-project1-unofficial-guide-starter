import os
import re
import json


def parse_files(data_folder="documents"):
    chunks = []

    for filename in os.listdir(data_folder):

        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(data_folder, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        professor_match = re.search(r"Professor:\s*(.+)", content)
        course_match = re.search(r"Course:\s*(.+)", content)

        professor = professor_match.group(1).strip() if professor_match else "Unknown"
        course = course_match.group(1).strip() if course_match else "Unknown"

        # FIX: split once outside the loop, keep delimiters with a capture group
        parts = re.split(r"(Review\s+\d+)", content)

        current_review_id = None

        for part in parts:
            part = part.strip()

            # Capture review header (e.g., "Review 1")
            if re.match(r"Review\s+\d+", part):
                current_review_id = part
                continue

            # Skip empty or tiny chunks
            if len(part) < 50:
                continue

            # Skip filler text
            if "No meaningful review content provided" in part:
                continue

            chunks.append({
                "professor": professor,
                "course": course,
                "review_id": current_review_id,
                "text": f"Professor: {professor}\nCourse: {course}\nReview: {current_review_id}\n\n{part}",
                "source": filename
            })

    return chunks


if __name__ == "__main__":
    chunks = parse_files()

    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(f"Saved {len(chunks)} chunks")

    if chunks:
        print("\nFirst chunk:\n")
        print(chunks[0]["professor"])
        print(chunks[0]["course"])
        print(chunks[0]["source"])
        print(chunks[0]["text"][:500])