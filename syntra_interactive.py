"""Interactive console for SYNTRA with detailed output.

TODO: expand with additional telemetry hooks once MODI/VALON
runtime APIs are finalized.
"""
from utils.repl import SyntraREPL
from utils.language_engine.core_brain import symbolic_dream_loop


def _post_cycle(_, __):
    dream = symbolic_dream_loop()
    print("\n🌙 DREAM OUTPUT:\n", dream)


def main() -> None:
    """Prompt the user and display VALON, MODI, DRIFT and DREAM segments."""
    repl = SyntraREPL(
        show_valon=True,
        show_modi=True,
        show_drift=True,
        post_cycle=_post_cycle,
    )
    repl.run()


if __name__ == "__main__":
    main()
