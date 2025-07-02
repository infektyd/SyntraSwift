import os
import time
import json
from datetime import datetime
from PyPDF2 import PdfReader
import sys
import subprocess
from utils.io_tools import load_config
from memory_engine import add_memory_node

# Define consistent paths
SOURCE_DIR = "source_pdfs"
MEMORY_VAULT = "memory_vault"
MODI_DIR = os.path.join(MEMORY_VAULT, "modi")
VALON_DIR = os.path.join(MEMORY_VAULT, "valon")
VALON_ARCHIVE = os.path.join(VALON_DIR, "valon_symbolic_archive.json")
ENTROPY_DIR = "entropy_logs"

# Create necessary directories
for directory in [SOURCE_DIR, MODI_DIR, VALON_DIR, ENTROPY_DIR]:
    os.makedirs(directory, exist_ok=True)

# Helper functions

def query_mistral(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral", prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"[ERROR] Mistral query failed: {e}")
        return f"Error: {str(e)}"

def query_chatgpt(prompt):
    try:
        config = load_config()
        import openai
        client = openai.OpenAI(
            api_key=config.get("openai_api_key", "lm-studio"),
            base_url=config.get("openai_api_base", "http://localhost:1234/v1")
        )
        response = client.chat.completions.create(
            model=config.get("openai_model", "phi-3-mini-4k-instruct"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[ERROR] ChatGPT query failed: {e}")
        return f"Error: {str(e)}"

def log_error(reason, filename):
    timestamp = datetime.now().isoformat()
    entry = {
        "timestamp": timestamp,
        "source": filename,
        "reason": reason,
        "flag": "processing_error"
    }
    log_path = os.path.join(ENTROPY_DIR, "processing_errors.json")
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(entry)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)
    print(f"[ERROR] {reason} for {filename}")

def extract_text_from_pdf(pdf_path):
    print(f"[INFO] Extracting text from {pdf_path}")
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- Page {i+1} ---\n{page_text}\n"
        return text
    except Exception as e:
        print(f"[ERROR] Failed to extract text: {e}")
        return None

def reflect_valon(content):
    return {
        "symbolic_terms": ["understanding", "mechanical", "procedure"],
        "emotions": ["focused", "technical", "methodical"],
        "structure": "procedural/informative",
        "meaning": "vehicle maintenance knowledge"
    }

def update_valon_archive(filename, reflection):
    if os.path.exists(VALON_ARCHIVE):
        with open(VALON_ARCHIVE, "r", encoding="utf-8") as f:
            archive = json.load(f)
    else:
        archive = {"symbolic_events": [], "drift_logs": [], "reasoning_blends": [], "dream_logs": []}
    archive["symbolic_events"].append({
        "source": filename,
        "reflected": reflection,
        "timestamp": datetime.now().isoformat()
    })
    with open(VALON_ARCHIVE, "w", encoding="utf-8") as f:
        json.dump(archive, f, indent=2)
    print(f"[INFO] Updated VALON archive with {filename}")

def process_pdf(filepath, filename, link=False):
    print(f"[INFO] Processing {filename}")
    content = extract_text_from_pdf(filepath)
    if not content:
        log_error("Failed to extract text", filename)
        return False

    print(f"[INFO] Generating full summary from chunked content for {filename}")
    chunk_size = 3000
    overlap = 500
    chunks = []
    start = 0
    while start < len(content):
        end = min(start + chunk_size, len(content))
        chunks.append(content[start:end])
        start += chunk_size - overlap

    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"[INFO] Summarizing chunk {i+1}/{len(chunks)}...")
        response = query_mistral(f"Summarize and extract key points from this section of a vehicle service manual:\n\n{chunk}")
        if "Error:" in response or "timed out" in response:
            print(f"[INFO] Mistral failed on chunk {i+1}, falling back to ChatGPT")
            response = query_chatgpt(f"Summarize and extract key points from this section of a vehicle service manual:\n\n{chunk}")
        summaries.append(f"--- Chunk {i+1} ---\n{response.strip()}")

    summary = "\n\n".join(summaries)

    reflection = reflect_valon(content)

    print(f"[INFO] Saving {filename} to MODI memory")
    entry = {
        "source": filename,
        "timestamp": datetime.now().isoformat(),
        "content_sample": content[:5000],
        "full_content_length": len(content),
        "summary": summary,
        "valon_reflection": reflection,
    }

    if link:
        assign_uid(entry)

    # Link to hybrid memory layer when enabled
    hybrid_uid = add_memory_node(entry)
    if hybrid_uid:
        entry["hybrid_uid"] = hybrid_uid
        if link:
            create_link(os.path.join(MODI_DIR, f"{filename.replace('.pdf', '')}.json"), hybrid_uid)

    modi_path = os.path.join(MODI_DIR, f"{filename.replace('.pdf', '')}.json")
    with open(modi_path, "w", encoding="utf-8") as f:
        json.dump(entry, f, indent=2)

    update_valon_archive(filename, reflection)

    valon_path = os.path.join(VALON_DIR, f"{filename.replace('.pdf', '')}.json")
    os.makedirs(os.path.dirname(valon_path), exist_ok=True)
    with open(valon_path, "w", encoding="utf-8") as f:
        json.dump({"summary": summary}, f, indent=2)

    print(f"[INFO] VALON summary saved to {valon_path}")
    print(f"[SUCCESS] {filename} processed successfully")
    return True

def process_directory(link=False):
    print(f"[INFO] Checking {SOURCE_DIR} for PDFs")
    processed = 0
    failed = 0
    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith(".pdf"):
            filepath = os.path.join(SOURCE_DIR, filename)
            if process_pdf(filepath, filename, link=link):
                processed += 1
            else:
                failed += 1
    print(f"[COMPLETE] Processed {processed} PDFs, {failed} failed")

def process_specific_file(filepath, link=False):
    filename = os.path.basename(filepath)
    if filename.endswith(".pdf"):
        if process_pdf(filepath, filename, link=link):
            print(f"[COMPLETE] Successfully processed {filename}")
        else:
            print(f"[COMPLETE] Failed to process {filename}")
    else:
        print(f"[ERROR] {filepath} is not a PDF file")

def main():
    print("[BOOT] Cintra PDF Ingestor has started.")
    link = '--link' in sys.argv
    if link:
        sys.argv.remove('--link')

    if len(sys.argv) > 1:
        if sys.argv[1] == '--watch':
            print("[WATCH] Entering folder monitor loop...")
        elif os.path.exists(sys.argv[1]) and sys.argv[1].endswith('.pdf'):
            process_specific_file(sys.argv[1], link=link)
        else:
            print(f"[ERROR] Invalid argument: {sys.argv[1]}")
    else:
        process_directory(link=link)

if __name__ == "__main__":
    main()
