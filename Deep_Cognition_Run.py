# VLD_PRIMITIVE: DeepCognitionRun
# CONTEXTUAL_USE: Omnidirectional ingestion and symbolic interpretation loop across MODI, VALON, SYNTRA
# DRIFT_RATIO: {"modi": 0.8, "valon": 0.2}

seen = set()
import logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
import os
import time
import json
import shutil
from telemetry_bridge import start_telemetry
import threading
from datetime import datetime
from PyPDF2 import PdfReader
#from ingest.pdf_ingestor import load_new_pdfs
from utils.pdf_ingest import watch_pdf_folder
from utils.mistral_bridge import query_mistral
from utils.entropy_guard import log_entropy_drift, trigger_dream
from utils.language_engine import (
    reflect_valon,
    reflect_modi,
    drift_average,
    log_drift,
    log_syntra,
)
from utils.dream_logger import log_dream



WATCH_FOLDER = "source_pdfs"
ARCHIVE_FOLDER = "processed_pdfs"
LOG_FOLDER = "syntra_debug_logs"

# Separate memory paths for each cognition node
MEMORY_MODI = "memory_vault/modi"
MEMORY_VALON = "memory_vault/valon"
VALON_ARCHIVE = os.path.join(MEMORY_VALON, "valon_symbolic_archive.json")

os.makedirs(ARCHIVE_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

def parse_pdf(filename, filepath):
    reader = PdfReader(filepath)
    parsed_text = ""
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            parsed_text += f"\n--- Page {i+1} ---\n{text}\n"
    return parsed_text

def load_new_pdfs(folder):
    docs = {}
    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            path = os.path.join(folder, filename)
            with open(path, "rb") as f:
                reader = PdfReader(f)
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
                docs[filename.replace(".pdf", "")] = text
    return docs

def run_loop():
    print("[SYNTRA] Beginning cognition loop...")
    learned_docs = load_new_pdfs("source_pdfs")
    for title, text in learned_docs.items():
        print(f"[SYNTRA] Ingested: {title}")
        # Save to vault or memory path
        with open(f"memory_vault/{title}.txt", "w", encoding="utf-8") as f:
            f.write(text)

    while True:
        files = set(os.listdir(WATCH_FOLDER))
        new_files = files - seen

        for filename in new_files:
            if filename.endswith(".pdf"):
                src_path = os.path.join(WATCH_FOLDER, filename)
                archive_path = os.path.join(ARCHIVE_FOLDER, filename)

                log_syntra(f"Ingesting {filename}", "MODI")
                try:
                    content = parse_pdf(filename, src_path)

                    out_path = os.path.join(MEMORY_MODI, f"{filename}.txt")
                    with open(out_path, "w", encoding="utf-8") as out:
                        out.write(content)

                    if os.path.exists(VALON_ARCHIVE):
                        with open(VALON_ARCHIVE, "r+", encoding="utf-8") as f:
                            archive = json.load(f)
                            archive["symbolic_events"].append({
                                "source": filename,
                                "reflected": reflect_valon(content),
                                "timestamp": datetime.now().isoformat()
                            })
                            f.seek(0)
                            json.dump(archive, f, indent=2)

                    log_syntra(f"WordNet/GPT review simulated for {filename}", "SYNTRA")
                    shutil.move(src_path, archive_path)
                    log_syntra(f"{filename} processed and archived", "MODI")

                except Exception as e:
                    log_syntra(f"ERROR processing {filename}: {e}", "SYNTRA")

        seen.update(new_files)
        user_input = input("[SYNTRA] Awaiting command (or 'exit'): ").strip().lower()
        if user_input == "exit":
            print("[SYNTRA] Termination confirmed.")
            log_syntra("Cognition loop exited by user.")
            break

        time.sleep(3)
        
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_deep_cognition():
    print("\n[DEEP LOOP] Initiating Deep Cognition Cycle...")

    # Traverse memory_vault for both cognition nodes
    brain_paths = {
        "valon": MEMORY_VALON,
        "modi": MEMORY_MODI,
    }
    for brain, brain_path in brain_paths.items():
        print(f"[DEEP LOOP] Analyzing {brain.title()} node memory at {brain_path}")

        for file in os.listdir(brain_path):
            if not file.endswith(".json"):
                continue

            full_path = os.path.join(brain_path, file)
            try:
                memory = load_json(full_path)
                thought_label = file.replace(".json", "")

                if brain == "valon":
                    insight = reflect_valon(thought_label, memory)
                else:
                    insight = reflect_modi(thought_label, memory)

                log_dream(brain, thought_label, insight)
                print(f"[DEEP LOOP] {brain.title()} reflected on '{thought_label}' → Logged.")
            
            except Exception as e:
                print(f"[ERROR] Failed to process {file}: {e}")

    print("\n[DEEP LOOP] Cycle Complete. Drift analysis logged into dreams.")

#threaded runtime
if __name__ == "__main__":
    try:
        telemetry_thread = start_telemetry()
        if telemetry_thread is not None:
            print("[DEEP LOOP] Telemetry thread active")
        pdf_thread = threading.Thread(target=watch_pdf_folder, daemon=True)
        pdf_thread.start()
        run_deep_cognition()

        run_loop()

    except Exception as e:
        print(f"[ERROR] SYNTRA crashed: {e}")
