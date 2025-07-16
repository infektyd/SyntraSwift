"""Simple REPL for interacting with SYNTRA."""

from utils.language_engine.language_core import run_language_cycle, run_language_loop
from utils.io_tools import load_config


class SyntraREPL:
    """Interactive loop to query SYNTRA."""

    def __init__(self, memory_engine=None, llm_bridge=None,
                 show_valon=None, show_modi=None, show_drift=None,
                 post_cycle=None):
        self.memory_engine = memory_engine
        self.llm_bridge = llm_bridge
        self.config = load_config()
        self.show_valon = show_valon
        self.show_modi = show_modi
        self.show_drift = show_drift
        self.post_cycle = post_cycle
        self.last_cognition = None

    def run_cycle(self, user_input: str):
        """Process a single user input through the language loop."""
        self.last_cognition = run_language_cycle(
            user_input,
            show_valon=self.show_valon,
            show_modi=self.show_modi,
            show_drift=self.show_drift,
        )
        return self.last_cognition["drift"]

    def run(self):
        """Prompt the user and print the DRIFT output."""
        while True:
            user_input = input("\n[SYNTRA] > ")
            if user_input.lower() in {"exit", "quit"}:
                break

            drift = self.run_cycle(user_input)
            print("\n🌀 Final Drift Output:\n", drift)
            if self.post_cycle:
                try:
                    self.post_cycle(user_input, drift)
                except Exception as exc:  # pragma: no cover - best effort
                    print(f"[SYNTRA] post_cycle error: {exc}")

