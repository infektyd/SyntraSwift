def log_syntra(msg):
    print(f"[SYNTRA] {msg}")


def log_drift(msg):
    print(f"[DRIFT] {msg}")


def log_entropy_event(event_type, file):
    print(f"[ENTROPY] Event '{event_type}' triggered by {file}")
