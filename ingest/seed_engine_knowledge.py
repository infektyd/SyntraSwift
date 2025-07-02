# seed_engine_knowledge.py
# Seeds SYNTRA Prime with knowledge from domain-specific PDFs and logs MODI reasoning

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  

import json
import shutil #python copy command, cross platform
from PyPDF2 import PdfReader
from utils.io_tools import load_config

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def classify_engine_by_filename(filename):
    if "63" in filename:
        return "TAMD63"
    if "71" in filename or "72" in filename:
        return "TAMD72"
    return "UNKNOWN_ENGINE"

def classify_subsystem_by_filename(filename):
    lowered = filename.lower()
    if "fuel" in lowered:
        return "fuel_system"
    elif "lube" in lowered or "lubrication" in lowered:
        return "lubrication_system"
    elif "air" in lowered:
        return "air_intake"
    elif "electrical" in lowered:
        return "electrical"
    else:
        return "general"

def seed_from_pdf_folder(folder_path):
    memory_root = os.path.join("memory", "VOLVO", "DIESEL", "MARINE")
    os.makedirs(memory_root, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            filepath = os.path.join(folder_path, filename)
            print(f"Processing {filename}...")

            engine = classify_engine_by_filename(filename)
            subsystem = classify_subsystem_by_filename(filename)

            engine_path = os.path.join(memory_root, engine)
            source_pdf_path = os.path.join(engine_path, "source_pdfs")
            subsystem_path = os.path.join(engine_path, "categories", subsystem)

            os.makedirs(source_pdf_path, exist_ok=True)
            os.makedirs(subsystem_path, exist_ok=True)

            # Save original PDF reference
            shutil.copy2(filepath, os.path.join(source_pdf_path, filename))

            # Extract and save raw text
            raw_text = extract_text_from_pdf(filepath)
            with open(os.path.join(subsystem_path, "raw_text.txt"), "w", encoding="utf-8") as f:
                f.write(raw_text)

            # Save index info
            index = {
                "engine": engine,
                "subsystem": subsystem,
                "filename": filename,
                "original_path": filepath
            }
            with open(os.path.join(subsystem_path, "index.json"), "w", encoding="utf-8") as f:
                json.dump(index, f, indent=2)

            # Save MODI reasoning
            reasoning = {
                "modi_weight": 0.9,
                "valon_weight": 0.1,
                "reason": f"Subsystem inferred from filename: '{filename}' → '{subsystem}'.",
                "engine_reason": f"Engine family determined from string match → '{engine}'.",
                "created_folders": [
                    source_pdf_path,
                    subsystem_path
                ]
            }
            with open(os.path.join(subsystem_path, "reasoning_log.json"), "w", encoding="utf-8") as f:
                json.dump(reasoning, f, indent=2)

if __name__ == "__main__":
    source_pdf_dir = "source_pdfs"
    seed_from_pdf_folder(source_pdf_dir)
