import os
import time
import json
from PyPDF2 import PdfReader
from datetime import datetime
from utils.mistral_bridge import query_mistral
from utils.language_engine import (
    reflect_valon,
    reflect_modi,
    drift_average,
    log_drift,
    log_syntra,
)
from memory_tools.index_linker import assign_uid, create_link


SOURCE_DIR = "source_pdfs"
DEST_DIR = "memory_vault/modi"

seen_files = set()

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def save_to_memory(file_name, content, link=False):
    timestamp = datetime.now().isoformat()
    print(f"[SYNTRA] Summary saved for {file_name}")
    print(f"[MISTRAL] Processing summary for {file_name}...")
    summary = query_mistral(f"Summarize and extract key terms:\n\n{content[:3000]}")
    # Inject reasoning logic
    valon_emotion = reflect_valon(content)
    modi_logic = reflect_modi(content)
    merged = drift_average(valon_emotion, modi_logic)

    log_drift(file_name, valon_emotion, modi_logic)
    log_syntra(f"[REASONING] Drift State: {merged['converged_state']}", "VALON_MODI")

    entry = {
        "source": file_name,
        "timestamp": timestamp,
        "raw_content": content,
        "mistral_summary": summary,
    }

    if link:
        assign_uid(entry)

    out_path = os.path.join(DEST_DIR, f"{file_name}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(entry, f, indent=2)

    if link:
        create_link(out_path, entry["uid"])

def watch_pdf_folder(link=False):
    print("[Ingest] Watching for new PDFs...")
    os.makedirs(DEST_DIR, exist_ok=True)

    while True:
        for file in os.listdir(SOURCE_DIR):
            if file.endswith(".pdf") and file not in seen_files:
                path = os.path.join(SOURCE_DIR, file)
                print(f"[Ingest] New PDF detected: {file}")
                try:
                    content = extract_text(path)
                    save_to_memory(file.replace(".pdf", ""), content, link=link)
                    seen_files.add(file)
                    print(f"[Ingest] {file} processed successfully.")
                except Exception as e:
                    print(f"[Ingest] Error processing {file}: {e}")
        time.sleep(5)


if __name__ == "__main__":
    import sys
    link_flag = "--link" in sys.argv
    if link_flag:
        sys.argv.remove("--link")
    watch_pdf_folder(link=link_flag)
