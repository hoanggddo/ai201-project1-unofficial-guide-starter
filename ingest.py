import os

def parse_files(data_folder='data'):
    chunks = []
    
    # Iterate through all files in the data directory
    for filename in os.listdir(data_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_folder, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Assume reviews are separated by a blank line
                # Change the split pattern if your files use a different delimiter
                raw_reviews = [r.strip() for r in content.split('\n\n') if r.strip()]
                
                for raw_text in raw_reviews:
                    # Logic to extract metadata (this depends on your file format)
                    # For this example, we assume the first line is Header: Value
                    lines = raw_text.split('\n')
                    metadata = {}
                    review_body = ""
                    
                    for line in lines:
                        if ":" in line:
                            key, val = line.split(":", 1)
                            metadata[key.strip().lower()] = val.strip()
                        else:
                            review_body += line + " "
                    
                    # Create the chunk object
                    chunk = {
                        "professor": metadata.get("professor", "Unknown"),
                        "course": metadata.get("course", "Unknown"),
                        "text": review_body.strip(),
                        "source": filename
                    }
                    chunks.append(chunk)
    return chunks

# Run and verify
if __name__ == "__main__":
    all_chunks = parse_files()
    print(f"Total chunks created: {len(all_chunks)}")
    
    print("\n--- Inspecting 5 Sample Chunks ---\n")
    for i, chunk in enumerate(all_chunks[:5]):
        print(f"Chunk {i+1}:")
        print(chunk)
        print("-" * 30)