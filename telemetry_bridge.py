"""Lightweight telemetry utilities."""

# pandas is optional; if missing the bridge simply no-ops
try:
    import pandas as pd
except Exception:  # pragma: no cover - import best effort
    pd = None
    print("[SYNTRA][Telemetry] pandas not available; telemetry disabled.")

TELEMETRY_ENABLED = pd is not None
import time
import os

from utils.io_tools import load_config

CONFIG = load_config()
CSV_PATH = CONFIG.get("telemetry_csv_path", r"C:\\HWiNFO_logs\\syntra_runtime.csv")
FIELDS_OF_INTEREST = [
    "CPU Package Power [W]",
    "GPU Power [W]",
    "GPU Memory Usage [%]",
    "Total GPU Power [% of TDP]",
    "Core 0 T0 Usage [%]",
    "Total CPU Usage [%]",
    "Memory Usage [%]",
    "Network: Intel I211AT - Total Bandwidth",
]

def extract_latest_metrics(csv_path):
    if not TELEMETRY_ENABLED:
        return {}
    if not os.path.exists(csv_path):
        print("[SYNTRA][Telemetry] CSV not found.")
        return {}

    try:
        df = pd.read_csv(csv_path)
        latest = df.tail(1)

        results = {}
        for field in FIELDS_OF_INTEREST:
            for col in latest.columns:
                if field.lower() in col.lower():
                    results[field] = latest[col].values[0]
                    break

        return results
    except Exception as e:
        print(f"[SYNTRA][Telemetry] Error reading log: {e}")
        return {}

def live_feed_to_syntra():
    if not TELEMETRY_ENABLED:
        return
    print("[SYNTRA][Telemetry] Bridge running...")
    while True:
        metrics = extract_latest_metrics(CSV_PATH)
        if metrics:
            print("[SYNTRA][Telemetry Feed]", metrics)  # Here we feed into cognition module
            # Example: send_to_cognition(metrics)
        time.sleep(2)  # Adjust based on polling rate

def start_telemetry():
    """Start the telemetry feed in a daemon thread."""
    if not TELEMETRY_ENABLED:
        print("[SYNTRA][Telemetry] Telemetry disabled.")
        return None
    import threading

    thread = threading.Thread(target=live_feed_to_syntra, daemon=True)
    thread.start()
    return thread
