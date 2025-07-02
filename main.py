from telemetry_bridge import start_telemetry
from utils.pdf_ingest import watch_pdf_folder
from run_SYNTRA_loop import main as run_loop
import threading

def main() -> None:
    """Entry point for running SYNTRA with background telemetry."""
    telemetry_thread = start_telemetry()
    pdf_thread = threading.Thread(target=watch_pdf_folder, daemon=True)
    pdf_thread.start()
    run_loop()


if __name__ == "__main__":
    main()
    